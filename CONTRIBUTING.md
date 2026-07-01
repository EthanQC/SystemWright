# Contributing to SystemWright

Thanks for helping improve SystemWright. It's a single cross-platform Agent Skill
(`SKILL.md` + references) plus its validators, CI, packaging, and landing page.

## Before you open a PR

Everything is dependency-free (no PyYAML, no network), so the full check set runs
on a bare clone. Run all of it and make sure it's green:

```sh
python3 quick_validate.py                 # structural validation (self-contained)
python3 scripts/test_validate_skill.py    # validator unit tests
python3 tests/check_skill_quality.py      # completeness / drift lint
python3 scripts/check_packaging.py        # manifests + landing-page validation
python3 -m py_compile scripts/*.py tests/check_skill_quality.py quick_validate.py && git diff --check
```

CI (`.github/workflows/ci.yml`) runs the same set on a clean checkout across
Python 3.9 and 3.12, and exercises the installer on every host path.

## Working rules

- **Branch — don't commit to `main` directly.** Open a topic branch and PR.
- **Keep it dependency-free and Python 3.9-clean** (the repo keeps
  `from __future__ import annotations`; no `match`, no runtime `X | Y`).
- **No machine-specific absolute paths** in any shipped file — the portability
  guard scans the skill body, references, both READMEs, the landing page, and the
  recorded runs.
- **Keep EN and zh-CN READMEs in sync.** The lint guards both; a section added to
  one must be added to the other.
- **The skill body stays under 500 lines**; push detail into `references/`.

## Editing the skill or references

If you change a section name, template field, or reference filename, update
`tests/check_skill_quality.py` (it asserts the load-bearing strings so the skill,
references, READMEs, and recorded runs cannot silently drift apart).

## Versioning

SystemWright is **unversioned by design.** There is no version field in the skill
metadata or the plugin manifests; releases are pinned by git commit on `main`
rather than a version number. Iterate on `main`; there is no changelog to maintain.
