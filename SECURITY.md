# Security Policy

SystemWright ships no runtime service and no executable that acts on its own.
It is an Agent Skill: instructions an AI agent (Claude Code, Codex, Gemini,
Cursor, …) reads to help a human design a work system. The security surface is
therefore the *guidance* — and the automations that guidance may lead a user to
build.

## What we care about

- **Guidance that would weaken a user's safety defaults.** The skill's core
  contract is that the minimal first version never performs an external
  real-world write (send, publish, pay, delete, modify production) without human
  approval, and that any MCP write primitive keeps its approval gate. A change
  that erodes those gates is a security issue, not just a quality one.
- **Prompt-injection / instruction-hijack surfaces** introduced by the skill or
  its references.
- **Machine-specific paths, secrets, or credentials** accidentally committed to
  the skill body, references, recorded runs, or scripts.

## Reporting

Please report privately rather than opening a public issue for anything
exploitable:

- Preferred: use GitHub's **private vulnerability reporting** on this repo
  (Security tab → "Report a vulnerability").
- Alternatively, open a minimal, non-sensitive issue asking a maintainer to make
  private contact — do not include exploit detail in the public issue.

We aim to acknowledge a report within a few days. Because there is no deployed
service, "remediation" means a corrected `SKILL.md` / reference / script merged to
`main`; installed copies update on the next `sh scripts/install.sh` or
`/plugin` update.

## Installing safely

Review `SKILL.md` and `references/` before installing — the skill is plain text
you can read end to end. The bundled installer copies the folder verbatim and
validates the result; it makes no network calls.
