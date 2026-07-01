#!/usr/bin/env python3
"""Completeness lint for the SystemWright skill.

Verifies the skill ships the templates, real trial outputs, negative-trigger
cases, cross-platform install docs, and license it promises — and that nothing
reintroduces a machine-specific path. Portable: the skill dir is auto-detected,
frontmatter is parsed by the shared loader in scripts/validate_skill.py, and
there are no absolute paths or third-party dependencies.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_skill import read_frontmatter, validate_skill  # noqa: E402


def find_skill_dir(root: Path) -> Path:
    candidates = [p for p in sorted(root.iterdir()) if (p / "SKILL.md").is_file()]
    if len(candidates) != 1:
        raise SystemExit(f"expected exactly one skill dir with SKILL.md, found: {[p.name for p in candidates]}")
    return candidates[0]


SKILL = find_skill_dir(ROOT)
REFERENCES = SKILL / "references"
TEST_OUTPUT = ROOT / "test-output"

SKILL_NAME = "system-wright"

# Phrases that only appear when the skill has produced a full design — their
# presence in a "should not trigger" response means it over-designed.
OVERDESIGN_MARKERS = [
    "work system card",
    "mcp decision",
    "orchestrator decision",
    "plain-language brief",
    "prompt layer",
    "context layer",
    "harness layer",
    "loop layer",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def require_contains(text: str, phrases: list[str], label: str, failures: list[str]) -> None:
    for phrase in phrases:
        require(phrase in text, f"{label} missing: {phrase}", failures)


def require_not_contains(text: str, phrases: list[str], label: str, failures: list[str]) -> None:
    for phrase in phrases:
        require(phrase not in text, f"{label} must not contain: {phrase}", failures)


def check_skill_entrypoint(failures: list[str]) -> None:
    text = read(SKILL / "SKILL.md")
    fm = read_frontmatter(SKILL)
    require(fm.get("name") == SKILL_NAME, f"SKILL.md name must be '{SKILL_NAME}' (got {fm.get('name')!r})", failures)

    ok, msg = validate_skill(SKILL)
    require(ok, f"skill fails structural validation: {msg}", failures)

    description = fm.get("description", "")
    require(description, "SKILL.md frontmatter description must exist", failures)
    require_contains(
        description,
        [
            "vague goal",
            "messy repeated workflow",
            "Do not use for one-off rewrites, pure definitions, temporary checklists, or ordinary code review",
        ],
        "SKILL.md description",
        failures,
    )
    require_contains(
        text,
        [
            "Plain-Language Brief",
            "Daily-Use Protocol",
            "references/daily-use-protocol.md",
            "audit/background only",
            "forbidden means",  # the anti-Goodhart Loop field
        ],
        "SKILL.md",
        failures,
    )


def check_references(failures: list[str]) -> None:
    daily = REFERENCES / "daily-use-protocol.md"
    require(daily.exists(), "daily-use-protocol.md must exist", failures)
    if daily.exists():
        require_contains(
            read(daily),
            ["Copyable Starting Prompt", "Plain-Language Output", "Daily-Use Protocol", "Markdown Record Template", "Review Rule"],
            "daily-use-protocol.md",
            failures,
        )

    require_contains(
        read(REFERENCES / "design-playbook.md"),
        ["Beginner Default Questions", "Plain-Language Brief Template", "MCP Primitive Decision Format", "Orchestrator Type Decision Format", "Forbidden means",
         "Permission tier", "Verification ladder", "Stop condition:", "Observability", "Grounding artifacts"],
        "design-playbook.md",
        failures,
    )
    require_not_contains(read(REFERENCES / "design-playbook.md"), ["### MCP Decision Format\n"], "design-playbook.md", failures)

    require_contains(
        read(REFERENCES / "four-layer-framework.md"),
        ["MCP primitive", "tool/resource/prompt", "control model", "manual/staged workflow / subagent / application orchestrator", "forbidden means",
         "Verification Ladder", "Permission Tiers", "Maker-Checker", "hill-climbing loop", "Observability"],
        "four-layer-framework.md",
        failures,
    )

    require_contains(
        read(REFERENCES / "failure-modes.md"),
        ["Runtime Failure Modes", "Goal failure", "Context failure", "Tool failure", "Verification failure",
         "Loop-control failure", "Memory failure", "Human-collaboration failure", "Economic failure",
         "verification ladder", "comprehension debt", "cognitive surrender"],
        "failure-modes.md",
        failures,
    )

    require_contains(
        read(REFERENCES / "research-notes.md"),
        ["Anthropic", "Claude Code Skills", "MCP Tools", "MCP Resources", "MCP Prompts", "OpenAI Agents SDK Orchestration", "Codex Subagents", "Official and Primary Standards"],
        "research-notes.md",
        failures,
    )

    require_contains(
        read(REFERENCES / "test-scenarios.md"),
        ["Should Trigger", "Should Not Trigger", "copyable starting prompt", "non-technical user", "negative examples", "SaaS Support Triage", "MCP = yes"],
        "test-scenarios.md",
        failures,
    )


def check_trial_output(path: Path, failures: list[str]) -> None:
    require_contains(
        read(path),
        [
            "Idea Diagnostic",
            # core Idea Diagnostic fields (must appear so spec-drift is caught)
            "Raw idea", "Real job", "Decision level", "Missing decisions",
            "Confirmation",
            "Plain-Language Brief",
            "Work System Card",
            "Prompt layer", "Context layer", "Harness layer", "Loop layer",
            "Human judgment gates",
            "MCP decision", "MCP primitive", "control model", "auth/data scope", "read/write side effects", "approval gate",
            "Orchestrator decision", "Orchestrator type",
            "Daily-Use Protocol", "Copyable Starting Prompt", "Markdown Record Template",
            "First task", "Review Rule",
            "Trial Run", "Observed capability", "Observed limitation",
            "manual/staged workflow",
        ],
        path.name,
        failures,
    )


def check_negative_triggers(failures: list[str]) -> None:
    negative = TEST_OUTPUT / "negative-trigger-tests.md"
    require(negative.exists(), "negative-trigger-tests.md must exist", failures)
    if not negative.exists():
        return
    text = read(negative)
    require_contains(text, ["Should Not Trigger", "Expected behavior", "Actual response", "Pass/fail", "do not over-design"], "negative-trigger-tests.md", failures)

    blocks = text.split("## Should Not Trigger:")[1:]
    require(len(blocks) >= 4, "negative-trigger-tests.md must have at least 4 should-not-trigger cases", failures)
    for block in blocks:
        lines = block.splitlines()
        title = lines[0].strip() if lines else "<empty>"
        for field in ("Input:", "Expected behavior:", "Actual response:", "Pass/fail:"):
            require(field in block, f"negative case {title} missing {field}", failures)
        if "Actual response:" not in block or "Pass/fail:" not in block:
            continue

        # Scan the WHOLE Actual-response section (between its header and Pass/fail:).
        response = block.split("Actual response:", 1)[1].split("Pass/fail:", 1)[0].strip()
        require(response, f"negative case {title} Actual response must not be empty", failures)

        verdict_tail = block.split("Pass/fail:", 1)[1].strip()
        tokens = verdict_tail.split()
        if not tokens:
            require(False, f"negative case {title} missing a Pass/fail verdict", failures)
            continue
        require(tokens[0].rstrip(".") == "Pass", f"negative case {title} must explicitly Pass", failures)

        lowered = response.lower()
        for marker in OVERDESIGN_MARKERS:
            require(marker not in lowered, f"negative response {title} shows over-design artifact: {marker!r}", failures)


def check_test_outputs(failures: list[str]) -> None:
    actual_tests = sorted(TEST_OUTPUT.glob("actual-test-*.md"))
    require(len(actual_tests) >= 3, "at least three actual-test-*.md outputs are required", failures)
    for path in actual_tests:
        check_trial_output(path, failures)

    combined = "\n".join(read(path) for path in actual_tests)
    require("xhs-ops-system" in combined, "actual tests must cover xhs-ops-system", failures)
    require("Founder" in combined or "founder" in combined, "actual tests must cover founder-level vague idea", failures)
    require("messy excerpt" in combined or "Messy excerpt" in combined, "actual tests must include a messy input", failures)
    # Stub detectors only (no value-judgment bans): a real run never says "should produce/return/include".
    require_not_contains(combined, ["should produce", "should return", "should include"], "actual test outputs", failures)

    xhs = TEST_OUTPUT / "actual-test-xhs-ops-system.md"
    if xhs.exists():
        require_contains(read(xhs), ["Actual run output", "Draft:", "Risk review:", "Approval gate:", "Memory update candidate:"], "actual-test-xhs-ops-system.md", failures)

    founder = TEST_OUTPUT / "actual-test-founder-level-idea.md"
    if founder.exists():
        require_contains(read(founder), ["Actual run output", "Weekly facts:", "Decision 1:", "Decision 2:", "Next-week check:"], "actual-test-founder-level-idea.md", failures)

    saas = TEST_OUTPUT / "actual-test-saas-support.md"
    if saas.exists():
        require_contains(read(saas), ["MCP needed: yes", "Verification ladder", "Permission tier", "Observability", "maker-checker", "Orchestrator decision", "Real 实测 protocol"], "actual-test-saas-support.md", failures)

    check_negative_triggers(failures)


def check_readme(failures: list[str]) -> None:
    text = read(ROOT / "README.md")
    require_contains(
        text,
        ["## Installation", "## Usage", "## Validation", "## Test Outputs", "## License"],
        "README.md sections",
        failures,
    )
    # Cross-platform: must document at least two hosts and the portable invocation.
    require_contains(
        text,
        [".claude/skills", ".codex/skills", "$system-wright", "scripts/install.sh"],
        "README.md cross-platform install",
        failures,
    )
    require_contains(
        text,
        [
            "test-output/actual-test-messy-ai-article-loop.md",
            "test-output/actual-test-xhs-ops-system.md",
            "test-output/actual-test-founder-level-idea.md",
            "test-output/negative-trigger-tests.md",
        ],
        "README.md test-output list",
        failures,
    )


def check_license(failures: list[str]) -> None:
    require((ROOT / "LICENSE").exists() or (ROOT / "LICENSE.md").exists(), "a LICENSE file must exist", failures)


def check_portability(failures: list[str]) -> None:
    # No user-home / machine-specific absolute paths in shipped docs or scripts.
    targets = [ROOT / "README.md", ROOT / "quick_validate.py"]
    targets += sorted((ROOT / "scripts").glob("*.py"))
    targets += sorted((ROOT / "scripts").glob("*.sh"))
    needle = "/" + "Users/"  # built at runtime so this guard file doesn't match itself
    for path in targets:
        if path.exists():
            require_not_contains(read(path), [needle], f"portability: {path.name}", failures)


def main() -> int:
    failures: list[str] = []
    check_skill_entrypoint(failures)
    check_references(failures)
    check_test_outputs(failures)
    check_readme(failures)
    check_license(failures)
    check_portability(failures)

    if failures:
        print("FAIL: skill quality checks found issues:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: skill quality checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
