#!/usr/bin/env python3
"""19 November 2026 world news, in one image.

Entry program for the make.fun news-image-20261119 bounty. It writes the
news-atlas image bundled in this repository to the output path the
bounty harness expects (/output/entry.png). Standard library only, no
network access, and fully deterministic: every run writes the same
bytes.
"""

import hashlib
import os
import shutil
import sys

IMAGE_NAME = "entry.png"


def _digest(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(1 << 16)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def _destination():
    for name in ("MAKEFUN_OUTPUT_DIR", "OUTPUT_DIR"):
        value = os.environ.get(name)
        if value:
            return os.path.join(value, IMAGE_NAME)
    return os.path.join("/output", IMAGE_NAME)


def run():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, IMAGE_NAME)
    target = _destination()
    os.makedirs(os.path.dirname(target), exist_ok=True)
    staging = target + ".part"
    shutil.copyfile(source, staging)
    if _digest(staging) != _digest(source):
        os.unlink(staging)
        print("copied image failed its checksum", file=sys.stderr)
        return 1
    os.replace(staging, target)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
