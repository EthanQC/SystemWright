#!/usr/bin/env python3
"""Validate this repository's skill with the bundled, self-contained validator.

No third-party dependencies and no machine-specific paths, so it runs on any
clone or CI. The skill directory is auto-detected (the single child of the repo
root that contains a SKILL.md), so renaming the skill needs no edit here.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))
from validate_skill import validate_skill  # noqa: E402


def find_skill_dir(root: Path) -> Path:
    candidates = [p for p in sorted(root.iterdir()) if (p / "SKILL.md").is_file()]
    if len(candidates) != 1:
        names = [p.name for p in candidates]
        raise SystemExit(f"expected exactly one skill directory with SKILL.md, found: {names}")
    return candidates[0]


def main() -> int:
    ok, msg = validate_skill(find_skill_dir(ROOT))
    print(msg)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
