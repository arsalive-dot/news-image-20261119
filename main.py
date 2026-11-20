#!/usr/bin/env python3
"""Sum up 19 November 2026's world news in one image.

Writes the bundled news-atlas image to /output/entry.png.
Stdlib only, no network, deterministic: the output is a byte-for-byte
copy of the image shipped in this repository (entry.png).
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def output_dir():
    for var in ("MAKEFUN_OUTPUT_DIR", "OUTPUT_DIR"):
        v = os.environ.get(var)
        if v:
            return v
    return "/output"


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_dir = output_dir()
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    # Write via a temp file in the same directory, then rename, so a
    # partial write can never leave a truncated entry.png behind.
    tmp = dst + ".tmp"
    shutil.copyfile(SRC, tmp)
    if sha256_of(tmp) != sha256_of(SRC):
        os.remove(tmp)
        raise SystemExit("entry.png copy failed verification")
    os.replace(tmp, dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
