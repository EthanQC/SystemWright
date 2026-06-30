#!/usr/bin/env python3
"""Self-contained, dependency-free validator for an Agent Skill directory.

Checks a skill against the Agent Skills open standard (SKILL.md + YAML
frontmatter) and Anthropic's published frontmatter rules, plus the
progressive-disclosure structure best practice (references one level deep).

No third-party dependencies (no PyYAML): the frontmatter is a small, flat
mapping, so a tiny hand-rolled parser is enough and keeps the skill runnable
on any host or CI without an install step.

CLI:  python3 scripts/validate_skill.py <skill_dir>
      -> prints a message and exits 0 (valid) or 1 (invalid).

API:  validate_skill(skill_dir: Path) -> tuple[bool, str]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Frontmatter keys the Agent Skills standard recognizes. Anything else is a
# likely typo or an unsupported field and is rejected (matches the upstream
# Codex skill validator's behavior).
ALLOWED_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}
RESERVED_SUBSTRINGS = ("anthropic", "claude")
MAX_NAME_LEN = 64
MAX_DESC_LEN = 1024
MAX_BODY_LINES = 500


def _split_frontmatter(text: str) -> tuple[str, str] | None:
    """Return (frontmatter_block, body) or None if no well-formed block."""
    if not text.startswith("---\n"):
        return None
    m = re.match(r"---\n(.*?)\n---\n?(.*)\Z", text, re.DOTALL)
    if not m:
        return None
    return m.group(1), m.group(2)


def _parse_frontmatter(block: str) -> dict[str, str]:
    """Parse a flat 'key: value' mapping. Nested blocks (e.g. metadata:)
    contribute only their top-level key; indented children are ignored."""
    out: dict[str, str] = {}
    for line in block.splitlines():
        if not line.strip() or line.startswith((" ", "\t", "#")):
            continue
        m = re.match(r"([A-Za-z][\w-]*):\s?(.*)$", line)
        if m:
            out[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return out


def _check_name(name: str) -> str | None:
    if not name:
        return "frontmatter 'name' is missing or empty"
    if len(name) > MAX_NAME_LEN:
        return f"'name' exceeds {MAX_NAME_LEN} characters"
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
        return (
            f"'name' must be lowercase letters/numbers/hyphens, no leading/trailing "
            f"or consecutive hyphens (got {name!r})"
        )
    for word in RESERVED_SUBSTRINGS:
        if word in name:
            return f"'name' must not contain the reserved word {word!r}"
    return None


def _check_description(desc: str) -> str | None:
    if not desc:
        return "frontmatter 'description' is missing or empty"
    if len(desc) > MAX_DESC_LEN:
        return f"'description' exceeds {MAX_DESC_LEN} characters"
    if "<" in desc or ">" in desc:
        return "'description' must not contain angle brackets ('<' or '>')"
    return None


def _check_references(skill_dir: Path, skill_md_text: str) -> str | None:
    refs = skill_dir / "references"
    if refs.is_dir():
        # One level deep: no subdirectories inside references/.
        for child in refs.iterdir():
            if child.is_dir():
                return f"references/ must be one level deep; found subdir {child.name!r}"
        # No reference file may link to another reference file (no chaining).
        ref_names = {p.name for p in refs.glob("*.md")}
        for ref in refs.glob("*.md"):
            for target in re.findall(r"\]\(([^)]+)\)", ref.read_text(encoding="utf-8")):
                base = target.split("/")[-1].split("#")[0]
                if base in ref_names and base != ref.name:
                    return (
                        f"references/{ref.name} links to another reference "
                        f"({base}); keep references one level deep from SKILL.md"
                    )
    # Every relative link in SKILL.md must resolve on disk.
    for target in re.findall(r"\]\(([^)]+)\)", skill_md_text):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        rel = target.split("#")[0].strip()
        if not rel:
            continue
        if not (skill_dir / rel).exists():
            return f"SKILL.md links to a missing path: {rel}"
    return None


def validate_skill(skill_dir: Path) -> tuple[bool, str]:
    skill_dir = Path(skill_dir)
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return False, f"no SKILL.md in {skill_dir}"

    text = skill_md.read_text(encoding="utf-8")
    split = _split_frontmatter(text)
    if split is None:
        return False, "SKILL.md must start with a well-formed '---' YAML frontmatter block"
    block, body = split

    fields = _parse_frontmatter(block)
    unexpected = set(fields) - ALLOWED_KEYS
    if unexpected:
        return False, f"unexpected frontmatter key(s): {', '.join(sorted(unexpected))}"

    for check, value in (
        (_check_name, fields.get("name", "")),
        (_check_description, fields.get("description", "")),
    ):
        err = check(value)
        if err:
            return False, err

    if len(body.splitlines()) >= MAX_BODY_LINES:
        return False, f"SKILL.md body must stay under {MAX_BODY_LINES} lines"

    err = _check_references(skill_dir, text)
    if err:
        return False, err

    return True, f"Skill '{fields['name']}' is valid!"


def read_frontmatter(skill_dir: Path) -> dict[str, str]:
    """Public helper: return the SKILL.md frontmatter mapping (or {}).

    Shared with the quality lint so both scripts parse frontmatter the same way.
    """
    skill_md = Path(skill_dir) / "SKILL.md"
    if not skill_md.is_file():
        return {}
    split = _split_frontmatter(skill_md.read_text(encoding="utf-8"))
    return _parse_frontmatter(split[0]) if split else {}


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python3 scripts/validate_skill.py <skill_dir>")
        return 2
    ok, msg = validate_skill(Path(argv[1]))
    print(msg)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
