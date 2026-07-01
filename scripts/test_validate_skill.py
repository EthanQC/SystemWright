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
from validate_skill import (  # noqa: E402
    find_skill_dir,
    read_frontmatter,
    validate_skill,
)
from validate_skill import main as cli_main  # noqa: E402


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

        # 18. Folded (block-scalar) description is accepted and length-checked.
        s = make_skill(
            tmp / "folded",
            "name: a-skill\ndescription: >\n"
            "  This is a folded description that spans two lines.\n"
            "  Use when testing block-scalar frontmatter parsing.",
        )
        expect("folded description accepted", validate_skill(s)[0], True)
        assert read_frontmatter(s)["description"].startswith("This is a folded"), "fold join"
        assert "\n" not in read_frontmatter(s)["description"], "folded value is single-lined"

        # 19. Oversized folded description is rejected (length measured on joined value).
        s = make_skill(
            tmp / "folded-long",
            "name: a-skill\ndescription: >\n  " + ("word " * 300),
        )
        expect("oversized folded description rejected", validate_skill(s)[0], False)

        # 20. A relative link inside a reference that points nowhere is rejected.
        s = make_skill(tmp / "refdangle", "name: a-skill\ndescription: x", body="# Title\n")
        refs = s / "references"
        refs.mkdir()
        (refs / "a.md").write_text("See [gone](missing-asset.md).\n", encoding="utf-8")
        expect("reference-internal dangling link rejected", validate_skill(s)[0], False)

        # 21. A subdirectory under references/ is rejected (one level deep).
        s = make_skill(tmp / "refsub", "name: a-skill\ndescription: x", body="# Title\n")
        (s / "references" / "sub").mkdir(parents=True)
        (s / "references" / "sub" / "deep.md").write_text("# deep\n", encoding="utf-8")
        expect("references subdirectory rejected", validate_skill(s)[0], False)

        # 22. allowed-tools: a well-formed token list passes; garbage/empty is rejected.
        s = make_skill(tmp / "tools-ok", "name: a-skill\ndescription: x\nallowed-tools: Read, Write, Bash")
        expect("valid allowed-tools accepted", validate_skill(s)[0], True)
        s = make_skill(tmp / "tools-bad", "name: a-skill\ndescription: x\nallowed-tools: <<>>garbage")
        expect("malformed allowed-tools rejected", validate_skill(s)[0], False)
        s = make_skill(tmp / "tools-empty", "name: a-skill\ndescription: x\nallowed-tools:")
        expect("empty allowed-tools rejected", validate_skill(s)[0], False)

        # 23. read_frontmatter returns {} when SKILL.md is absent.
        expect("read_frontmatter empty on missing SKILL.md", read_frontmatter(tmp / "empty") == {}, True)

        # 24. find_skill_dir locates the single skill dir under a root.
        root = tmp / "root"
        (root / "the-skill").mkdir(parents=True)
        (root / "the-skill" / "SKILL.md").write_text(
            "---\nname: a-skill\ndescription: x\n---\n\n# T\n", encoding="utf-8"
        )
        expect("find_skill_dir finds the skill", find_skill_dir(root).name == "the-skill", True)

        # 25. CLI main() exit codes: valid -> 0, invalid -> 1, wrong argc -> 2.
        good = make_skill(tmp / "cli-ok", "name: a-skill\ndescription: Does a thing. Use when testing.")
        bad = make_skill(tmp / "cli-bad", "name: BadName\ndescription: x")
        expect("main() returns 0 for valid", cli_main(["prog", str(good)]) == 0, True)
        expect("main() returns 1 for invalid", cli_main(["prog", str(bad)]) == 1, True)
        expect("main() returns 2 for wrong argc", cli_main(["prog"]) == 2, True)

    print(f"PASS {len(PASSES)} / {len(PASSES) + len(FAILS)}")
    if FAILS:
        print("FAILED CASES:")
        for f in FAILS:
            print(f"  - {f}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
