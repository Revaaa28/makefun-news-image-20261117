#!/usr/bin/env python3
"""news-image-20261117 entry program.

The entry image is a one-page broadsheet summing up Tuesday 17 November
2026, drawn programmatically by compose.py and committed here as
entry.png. This program installs that committed image as the entry
artifact: it copies entry.png into the output directory (the directory
named by MAKEFUN_OUTPUT_DIR, or /output by default).

Standard library only; no network; deterministic — the same bytes are
written on every run.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGE = os.path.join(HERE, "entry.png")


def main():
    if not os.path.isfile(IMAGE):
        print(f"error: committed entry image not found: {IMAGE}", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(IMAGE, dest)
    print(f"wrote {dest} ({os.path.getsize(dest)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
