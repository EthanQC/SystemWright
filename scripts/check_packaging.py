#!/usr/bin/env python3
"""Validate the distribution artifacts the skill body checks do not cover.

check_skill_quality.py validates SKILL.md + references; this guards the files
that actually govern how the skill is shipped and found: the Claude plugin
manifests, the Codex display metadata, and the GitHub Pages landing page. A
malformed manifest or a description/keyword/homepage that has drifted out of
sync with SKILL.md would otherwise ship on green CI and break `/plugin` install
or the browsing surface.

Dependency-free (stdlib json + a tiny line reader for the one YAML file, no
PyYAML) and no network, so it runs on any clone or CI.

Run: python3 scripts/check_packaging.py  -> exits 0 (ok) or 1 (issues).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_skill import find_skill_dir, read_frontmatter  # noqa: E402

MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
PLUGIN = find_skill_dir(ROOT) / ".claude-plugin" / "plugin.json"
OPENAI_YAML = find_skill_dir(ROOT) / "openai.yaml"
LANDING = ROOT / "docs" / "index.html"

SKILL_NAME = "system-wright"
HOMEPAGE = "https://ethanqc.github.io/SystemWright/"
DESC_CORE = "Prompt, Context, Harness, and Loop"
# Every advertised host must be discoverable via keywords.
REQUIRED_KEYWORDS = {"claude-code", "codex", "gemini", "cursor"}


def require(cond: bool, message: str, failures: list[str]) -> None:
    if not cond:
        failures.append(message)


def load_json(path: Path, failures: list[str]) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - report any parse/read error as a failure
        failures.append(f"{path.relative_to(ROOT)} is not valid JSON: {exc}")
        return {}


def check_manifests(failures: list[str]) -> None:
    market = load_json(MARKETPLACE, failures)
    plugin = load_json(PLUGIN, failures)
    if not market or not plugin:
        return

    plugins = market.get("plugins") or []
    require(len(plugins) == 1, f"marketplace.json must list exactly one plugin (found {len(plugins)})", failures)
    if not plugins:
        return
    entry = plugins[0]

    # Names / source.
    require(market.get("name") == SKILL_NAME, f"marketplace top-level name must be {SKILL_NAME!r}", failures)
    require(entry.get("name") == SKILL_NAME, f"marketplace plugin name must be {SKILL_NAME!r}", failures)
    require(plugin.get("name") == SKILL_NAME, f"plugin.json name must be {SKILL_NAME!r}", failures)
    require(entry.get("source") == "./system-wright", "marketplace plugin source must be './system-wright'", failures)

    # Cross-manifest agreement (the drift these fields silently accrue).
    for field in ("description", "homepage", "license"):
        require(
            entry.get(field) == plugin.get(field),
            f"marketplace and plugin.json disagree on {field!r}: {entry.get(field)!r} vs {plugin.get(field)!r}",
            failures,
        )
    require(
        (entry.get("author") or {}).get("name") == (plugin.get("author") or {}).get("name"),
        "marketplace and plugin.json disagree on author.name",
        failures,
    )
    require(plugin.get("homepage") == HOMEPAGE, f"plugin.json homepage must be {HOMEPAGE!r}", failures)
    require(plugin.get("license") == "MIT", "plugin.json license must be 'MIT'", failures)

    # Descriptions carry the shared four-layer core (guards positioning drift vs SKILL.md).
    fm_desc = read_frontmatter(find_skill_dir(ROOT)).get("description", "")
    require(DESC_CORE in fm_desc, f"SKILL.md description must contain {DESC_CORE!r}", failures)
    require(DESC_CORE in (plugin.get("description") or ""), f"plugin.json description must contain {DESC_CORE!r}", failures)
    require(DESC_CORE in (entry.get("description") or ""), f"marketplace description must contain {DESC_CORE!r}", failures)

    # Keywords: every advertised host discoverable, and both files agree.
    market_kw = set(entry.get("keywords") or [])
    plugin_kw = set(plugin.get("keywords") or [])
    missing_market = REQUIRED_KEYWORDS - market_kw
    missing_plugin = REQUIRED_KEYWORDS - plugin_kw
    require(not missing_market, f"marketplace keywords missing advertised host(s): {sorted(missing_market)}", failures)
    require(not missing_plugin, f"plugin.json keywords missing advertised host(s): {sorted(missing_plugin)}", failures)
    require(market_kw == plugin_kw, "marketplace and plugin.json keyword sets differ", failures)


def check_openai_yaml(failures: list[str]) -> None:
    require(OPENAI_YAML.is_file(), "system-wright/openai.yaml must exist", failures)
    if not OPENAI_YAML.is_file():
        return
    text = OPENAI_YAML.read_text(encoding="utf-8")
    for key in ("interface:", "display_name:", "short_description:", "default_prompt:"):
        require(key in text, f"openai.yaml must define {key!r}", failures)
    # The Codex explicit-invocation token must match the skill name.
    prompt_line = next((ln for ln in text.splitlines() if ln.strip().startswith("default_prompt:")), "")
    require("$system-wright" in prompt_line, "openai.yaml default_prompt must invoke '$system-wright'", failures)


def check_landing(failures: list[str]) -> None:
    require(LANDING.is_file(), "docs/index.html must exist", failures)
    if not LANDING.is_file():
        return
    html = LANDING.read_text(encoding="utf-8")
    require(bool(html.strip()), "docs/index.html must not be empty", failures)
    require("<title>" in html, "docs/index.html must have a <title>", failures)
    require('rel="canonical"' in html, "docs/index.html must set a canonical link", failures)
    # The og:image, if a repo-relative asset, must actually exist on disk.
    m = re.search(r'property="og:image"\s+content="[^"]*/([^"/]+)"', html)
    if m:
        asset = m.group(1)
        require((LANDING.parent / asset).is_file(), f"docs/{asset} (og:image) is referenced but missing", failures)


def main() -> int:
    failures: list[str] = []
    check_manifests(failures)
    check_openai_yaml(failures)
    check_landing(failures)

    if failures:
        print("FAIL: packaging checks found issues:")
        for f in failures:
            print(f"- {f}")
        return 1
    print("PASS: packaging + landing-page checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
