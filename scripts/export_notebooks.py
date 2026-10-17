#!/usr/bin/env python3
"""Export lecture notebooks (notebooks/*.qmd) as clean Jupyter notebooks.

Runs as a Quarto pre-render script of a slides project (ru/slides, en/slides).
Each notebooks/<name>.qmd becomes notebooks/<name>.ipynb next to it (git-ignored,
published as a project resource) without outputs: students download it and run
the cells themselves. The YAML header becomes a title cell; Quarto cell options
(#| lines) are dropped.

As a post-render script (Quarto sets QUARTO_PROJECT_OUTPUT_FILES) it rewrites
the absolute source paths that {{< embed >}} leaves in data-notebook attributes
of the rendered HTML to paths relative to the project.

Usage outside Quarto: python scripts/export_notebooks.py <project-dir>
"""

import json
import os
import re
import sys
from pathlib import Path

CHUNK_START = re.compile(r"^```\{python[^}]*\}\s*$")
CHUNK_END = re.compile(r"^```\s*$")


def front_matter(lines):
    if not lines or lines[0].strip() != "---":
        return {}, lines
    end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    meta = {}
    for line in lines[1:end]:
        m = re.match(r'^(title|subtitle|author):\s*"?(.*?)"?\s*$', line)
        if m:
            meta[m.group(1)] = m.group(2)
    return meta, lines[end + 1:]


def markdown_cell(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text}


def code_cell(text):
    return {"cell_type": "code", "execution_count": None, "metadata": {},
            "outputs": [], "source": text}


def split_source(text):
    return [line + "\n" for line in text.split("\n")[:-1]] + [text.split("\n")[-1]]


def convert(qmd: Path) -> dict:
    meta, body = front_matter(qmd.read_text(encoding="utf-8").splitlines())
    title = [f"# {meta.get('title', qmd.stem)}"]
    byline = " · ".join(v for v in (meta.get("subtitle"), meta.get("author")) if v)
    if byline:
        title += ["", f"*{byline}*"]
    cells = [markdown_cell("\n".join(title))]

    text, code, in_code = [], [], False
    for line in body:
        if not in_code and CHUNK_START.match(line):
            if "\n".join(text).strip():
                cells.append(markdown_cell("\n".join(text).strip()))
            text, code, in_code = [], [], True
        elif in_code and CHUNK_END.match(line):
            cells.append(code_cell("\n".join(code).strip()))
            in_code = False
        elif in_code:
            if not line.startswith("#|"):
                code.append(line)
        else:
            text.append(line)
    if "\n".join(text).strip():
        cells.append(markdown_cell("\n".join(text).strip()))

    for i, cell in enumerate(cells):
        cell["id"] = f"cell-{i:02d}"
        cell["source"] = split_source(cell["source"])
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python",
                           "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def strip_source_paths(project: Path, outputs):
    prefix = f'data-notebook="{project.resolve()}/'
    for name in outputs:
        html = Path(name)
        if html.suffix != ".html" or not html.is_file():
            continue
        text = html.read_text(encoding="utf-8")
        if prefix in text:
            html.write_text(text.replace(prefix, 'data-notebook="'), encoding="utf-8")


def main():
    project = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    outputs = os.environ.get("QUARTO_PROJECT_OUTPUT_FILES")
    if outputs is not None:
        strip_source_paths(project, outputs.splitlines())
        return
    for qmd in sorted((project / "notebooks").glob("*.qmd")):
        target = qmd.with_suffix(".ipynb")
        target.write_text(json.dumps(convert(qmd), ensure_ascii=False, indent=1) + "\n",
                          encoding="utf-8")
        print(f"notebook: {target.relative_to(project)}")


if __name__ == "__main__":
    main()
