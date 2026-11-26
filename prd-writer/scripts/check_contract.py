"""Check the structure of this release bundle using the Python standard library."""

import re
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    entry = root / "SKILL.md"
    template = root / "references/prd-template.md"
    entry_text = entry.read_text(encoding="utf-8") if entry.is_file() else ""
    template_text = template.read_text(encoding="utf-8") if template.is_file() else ""
    frontmatter = entry_text.split("---", 2)
    metadata = frontmatter[1] if len(frontmatter) == 3 and not frontmatter[0] else ""
    version = re.search(r'^  version: "(\d+\.\d+(?:\.\d+)?)"$', metadata, re.MULTILINE)
    template_version = re.search(r"^> 模板版本：V([\d.]+)。", template_text, re.MULTILINE)
    resources = (
        "references/prd-template.md",
        "references/prompts.md",
        "references/feature-list-template.md",
        "references/quality-checklist.md",
        "references/prototype-guide.md",
    )
    checks = {
        "name": bool(re.search(r"^name: prd-writer$", metadata, re.MULTILINE)),
        "version_alignment": bool(
            version and template_version and version[1] == template_version[1]
        ),
        "chapter_structure": re.findall(
            r"^## (\d{2}) ", template_text, re.MULTILINE
        ) == [f"{chapter:02d}" for chapter in range(11)],
        "resources": all((root / path).is_file() for path in resources),
    }
    for label, passed in checks.items():
        print(f"{'PASS' if passed else 'FAIL'} {label}")
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
