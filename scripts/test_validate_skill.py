#!/usr/bin/env python3
"""Tests for the self-contained, dependency-free skill validator.

Run: python3 scripts/test_validate_skill.py
Exits 0 if all behaviors hold, 1 otherwise. No third-party deps.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_skill import validate_skill  # noqa: E402


PASSES: list[str] = []
FAILS: list[str] = []


def make_skill(tmp: Path, frontmatter: str, body: str = "# Title\n\nHello.\n") -> Path:
    skill = tmp / "a-skill"
    skill.mkdir(parents=True, exist_ok=True)
    (skill / "SKILL.md").write_text(f"---\n{frontmatter}\n---\n\n{body}", encoding="utf-8")
    return skill


def expect(label: str, ok: bool, want_ok: bool) -> None:
    (PASSES if ok == want_ok else FAILS).append(label)


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]

    # 1. The real, shipped skill must validate.
    real = next(p for p in repo_root.iterdir() if (p / "SKILL.md").exists())
    ok, msg = validate_skill(real)
    expect(f"real skill '{real.name}' validates (msg={msg!r})", ok, True)

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)

        # 2. Minimal well-formed skill passes.
        s = make_skill(tmp / "ok", "name: a-skill\ndescription: Does a thing. Use when testing.")
        expect("minimal valid skill passes", validate_skill(s)[0], True)

        # 3. Uppercase letters in name are rejected.
        s = make_skill(tmp / "upper", "name: SystemWright\ndescription: x")
        expect("uppercase name rejected", validate_skill(s)[0], False)

        # 4. Reserved words (anthropic/claude) rejected.
        s = make_skill(tmp / "rsv", "name: claude-helper\ndescription: x")
        expect("reserved word 'claude' rejected", validate_skill(s)[0], False)

        # 5. Leading/trailing hyphen rejected.
        s = make_skill(tmp / "hyph", "name: -bad-\ndescription: x")
        expect("edge hyphen rejected", validate_skill(s)[0], False)

        # 6. Consecutive hyphens rejected.
        s = make_skill(tmp / "dh", "name: a--b\ndescription: x")
        expect("consecutive hyphen rejected", validate_skill(s)[0], False)

        # 7. Name over 64 chars rejected.
        s = make_skill(tmp / "long", f"name: {'a' * 65}\ndescription: x")
        expect("name >64 chars rejected", validate_skill(s)[0], False)

        # 8. Missing name rejected.
        s = make_skill(tmp / "noname", "description: x")
        expect("missing name rejected", validate_skill(s)[0], False)

        # 9. Missing description rejected.
        s = make_skill(tmp / "nodesc", "name: a-skill")
        expect("missing description rejected", validate_skill(s)[0], False)

        # 10. Angle brackets in description rejected.
        s = make_skill(tmp / "ab", "name: a-skill\ndescription: do <x> things")
        expect("angle brackets in description rejected", validate_skill(s)[0], False)

        # 11. Unexpected frontmatter key rejected.
        s = make_skill(tmp / "key", "name: a-skill\ndescription: x\nbogus: 1")
        expect("unexpected frontmatter key rejected", validate_skill(s)[0], False)

        # 12. Allowed optional keys (license, metadata) pass.
        s = make_skill(
            tmp / "meta",
            "name: a-skill\ndescription: x\nlicense: MIT\nmetadata:\n  author: x\n  version: 1.0.0",
        )
        expect("license + metadata keys allowed", validate_skill(s)[0], True)

        # 13. Missing SKILL.md rejected.
        empty = tmp / "empty"
        empty.mkdir()
        expect("missing SKILL.md rejected", validate_skill(empty)[0], False)

        # 14. No frontmatter rejected.
        nofm = tmp / "nofm"
        nofm.mkdir()
        (nofm / "SKILL.md").write_text("# just a title\n", encoding="utf-8")
        expect("missing frontmatter rejected", validate_skill(nofm)[0], False)

        # 15. Body >=500 lines rejected.
        s = make_skill(tmp / "big", "name: a-skill\ndescription: x", body="x\n" * 500)
        expect("body >=500 lines rejected", validate_skill(s)[0], False)

        # 16. Nested reference (a reference linking to another reference) rejected.
        s = make_skill(
            tmp / "nest",
            "name: a-skill\ndescription: x",
            body="See [a](references/a.md)\n",
        )
        refs = s / "references"
        refs.mkdir()
        (refs / "a.md").write_text("See [b](b.md) for more.\n", encoding="utf-8")
        (refs / "b.md").write_text("# B\n", encoding="utf-8")
        expect("nested reference link rejected", validate_skill(s)[0], False)

        # 17. SKILL.md linking to a missing reference rejected.
        s = make_skill(
            tmp / "dangling",
            "name: a-skill\ndescription: x",
            body="See [x](references/missing.md)\n",
        )
        (s / "references").mkdir()
        expect("dangling reference link rejected", validate_skill(s)[0], False)

    print(f"PASS {len(PASSES)} / {len(PASSES) + len(FAILS)}")
    if FAILS:
        print("FAILED CASES:")
        for f in FAILS:
            print(f"  - {f}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
