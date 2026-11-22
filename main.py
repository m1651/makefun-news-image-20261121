"""Entry program for the 21 November 2026 world-news image.

Copies the finished picture, entry.png, from this repository into the
directory make.fun names in MAKEFUN_OUTPUT_DIR (or /output by default),
under the same name. Standard library only; no network, no other files.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.png")
    shutil.copyfile(source, target)
    print("wrote", target, os.path.getsize(target), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
