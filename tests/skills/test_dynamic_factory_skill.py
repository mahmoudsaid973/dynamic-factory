"""Validate the Dynamic Factory Hermes skill package."""
import ast
import re
from pathlib import Path

import pytest
import yaml

SKILL_DIR = Path("skills/autonomous-ai-agents/dynamic-factory")
SKILL_FILE = SKILL_DIR / "SKILL.md"
SCRIPT_FILE = SKILL_DIR / "scripts" / "create_and_run.py"


def test_skill_file_exists() -> None:
    assert SKILL_FILE.exists()
    assert SKILL_FILE.read_text(encoding="utf-8").strip()


def test_frontmatter_valid() -> None:
    content = SKILL_FILE.read_text(encoding="utf-8")
    assert content.startswith("---")
    match = re.search(r"\n---\s*\n", content[3:])
    assert match, "frontmatter closing delimiter not found"

    frontmatter_text = content[3 : 3 + match.start()]
    frontmatter = yaml.safe_load(frontmatter_text)
    assert isinstance(frontmatter, dict)

    assert frontmatter.get("name") == "dynamic-factory"
    assert "description" in frontmatter
    description = frontmatter["description"]
    assert description.endswith(".")
    assert len(description) <= 60

    platforms = set(frontmatter.get("platforms", []))
    assert platforms >= {"linux", "macos", "windows"}

    assert "version" in frontmatter
    assert "author" in frontmatter
    assert "license" in frontmatter
    assert "metadata" in frontmatter
    assert frontmatter["metadata"]["hermes"]["tags"]


def test_helper_script_exists_and_parses() -> None:
    assert SCRIPT_FILE.exists()
    source = SCRIPT_FILE.read_text(encoding="utf-8")
    ast.parse(source)
