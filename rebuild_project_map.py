from __future__ import annotations

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime

# ==========================
# CONFIG
# ==========================

ROOT = Path(__file__).resolve().parent

WORKFLOW_DIR = ROOT / "workflow"
MAP_MD = WORKFLOW_DIR / "PROJECT_MAP_FULL.md"
MAP_JSON = WORKFLOW_DIR / "PROJECT_MAP_FULL.json"
WORKING_MEMORY = WORKFLOW_DIR / "PROJECT_WORKING_MEMORY.md"

IGNORE_DIRS = {
    ".git", ".hg", ".svn",
    "__pycache__", ".pytest_cache", ".mypy_cache",
    ".venv", "venv", "env",
    "node_modules",
}

IGNORE_FILES = {
    ".DS_Store",
}

HASH_MAX_BYTES = 2_000_000

AUTO_START = "<!-- AUTO:PROJECT_MAP_START -->"
AUTO_END = "<!-- AUTO:PROJECT_MAP_END -->"
APPEND_LOG_START = "<!-- APPEND_LOG_START -->"


# ==========================
# HELPERS
# ==========================

def safe_rel(p: Path) -> str:
    return str(p.resolve().relative_to(ROOT.resolve())).replace("/", "\\")


def sha256_short(path: Path) -> str | None:
    try:
        if path.stat().st_size > HASH_MAX_BYTES:
            return None
        h = hashlib.sha256()
        with path.open("rb") as f:
            h.update(f.read())
        return h.hexdigest()[:12]
    except Exception:
        return None


def count_lines_if_text(path: Path) -> int | None:
    if path.suffix.lower() in {".py", ".md", ".txt", ".json", ".csv"}:
        try:
            with path.open("r", encoding="utf-8", errors="ignore") as f:
                return sum(1 for _ in f)
        except Exception:
            return None
    return None


def is_ignored_dir(name: str) -> bool:
    if name in IGNORE_DIRS:
        return True
    if name.startswith(".") and name not in {"workflow", "docs"}:
        return True
    return False


# ==========================
# SCAN
# ==========================

def scan_tree(root: Path):
    items = []

    for cur_dir, subdirs, files in os.walk(root):
        subdirs[:] = [d for d in subdirs if not is_ignored_dir(d)]
        cur_path = Path(cur_dir)

        if cur_path != root:
            items.append({"type": "dir", "path": safe_rel(cur_path)})

        for fn in files:
            if fn in IGNORE_FILES:
                continue
            p = cur_path / fn
            try:
                st = p.stat()
            except Exception:
                continue

            items.append({
                "type": "file",
                "path": safe_rel(p),
                "size_bytes": st.st_size,
                "mtime": datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"),
                "lines": count_lines_if_text(p),
                "sha256_12": sha256_short(p),
            })

    return items


def summarize(items):
    files = [x for x in items if x["type"] == "file"]
    dirs = [x for x in items if x["type"] == "dir"]

    largest = sorted(files, key=lambda f: f["size_bytes"], reverse=True)[:5]

    return {
        "files": len(files),
        "dirs": len(dirs),
        "largest_files": largest,
    }


# ==========================
# RENDER
# ==========================

def render_map_md(items, summary):
    now = datetime.now().isoformat(timespec="seconds")
    out = []
    out.append("# PROJECT MAP — FULL\n\n")
    out.append(f"Generated: {now}\n\n")
    out.append(f"Root: {ROOT}\n\n---\n\n")

    out.append("## Summary\n")
    out.append(f"- Files: {summary['files']}\n")
    out.append(f"- Dirs: {summary['dirs']}\n")
    out.append("\n### Largest files\n")
    for f in summary["largest_files"]:
        out.append(f"- {f['path']} ({f['size_bytes']} bytes)\n")

    out.append("\n---\n\n## Full listing\n\n")

    for x in items:
        if x["type"] == "dir":
            out.append(f"- dir  | {x['path']}\n")
        else:
            out.append(
                f"- file | {x['path']} | {x['size_bytes']} | "
                f"{x['mtime']} | {x['lines'] or ''} | {x['sha256_12'] or ''}\n"
            )

    return "".join(out)


def update_working_memory(summary):
    if not WORKING_MEMORY.exists():
        return

    text = WORKING_MEMORY.read_text(encoding="utf-8", errors="ignore")

    auto_block = (
        f"{AUTO_START}\n"
        "## PROJECT STRUCTURE SNAPSHOT (AUTO)\n"
        f"Updated: {datetime.now().isoformat(timespec='seconds')}\n\n"
        f"- Files: {summary['files']}\n"
        f"- Dirs: {summary['dirs']}\n"
        f"- Map MD: workflow\\PROJECT_MAP_FULL.md\n"
        f"- Map JSON: workflow\\PROJECT_MAP_FULL.json\n\n"
        f"{AUTO_END}\n"
    )

    if AUTO_START in text and AUTO_END in text:
        before = text.split(AUTO_START)[0]
        after = text.split(AUTO_END)[1]
        text = before + auto_block + after
    else:
        text += "\n\n" + auto_block

    if APPEND_LOG_START not in text:
        text += (
            f"\n{APPEND_LOG_START}\n"
            "## APPEND-ONLY LOG (USER)\n"
            "- Dopisuj nowe wpisy poniżej.\n"
            "- Starsze wpisy będą okresowo konsolidowane.\n\n"
        )

    WORKING_MEMORY.write_text(text, encoding="utf-8")


# ==========================
# MAIN
# ==========================

def main():
    WORKFLOW_DIR.mkdir(parents=True, exist_ok=True)

    items = scan_tree(ROOT)
    summary = summarize(items)

    MAP_JSON.write_text(
        json.dumps(
            {"generated": datetime.now().isoformat(), "items": items, "summary": summary},
            indent=2
        ),
        encoding="utf-8",
    )

    MAP_MD.write_text(render_map_md(items, summary), encoding="utf-8")

    update_working_memory(summary)

    print("[OK] PROJECT_MAP_FULL.md generated")
    print("[OK] PROJECT_MAP_FULL.json generated")
    if WORKING_MEMORY.exists():
        print("[OK] PROJECT_WORKING_MEMORY.md updated")


if __name__ == "__main__":
    main()