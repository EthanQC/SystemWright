<!-- Thanks for contributing to SystemWright! -->

## What this changes

<!-- One or two sentences. Link any issue it closes: "Closes #123". -->

## Type

- [ ] Skill / reference content (`SKILL.md`, `references/`)
- [ ] Validators / tests / CI
- [ ] Packaging (manifests, installer, landing page)
- [ ] Docs (README EN/zh-CN)

## Checklist

- [ ] Ran the full check set green (see `CONTRIBUTING.md`):
      `quick_validate.py`, `test_validate_skill.py`, `check_skill_quality.py`,
      `check_packaging.py`, and `py_compile … && git diff --check`.
- [ ] No machine-specific absolute paths added.
- [ ] EN and zh-CN READMEs kept in sync (if either changed).
- [ ] If I renamed a section / field / reference file, I updated
      `tests/check_skill_quality.py` accordingly.
- [ ] Branch is off `main` (not committing to `main` directly).
