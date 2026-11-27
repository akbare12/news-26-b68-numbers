"""Entry point for news-image-20261126, variant b68.

The image is rendered at build time by gen.py and shipped in this
repository as entry.png. This program only copies that file into the
output directory the grader provides, using the standard library.

The grader runs with no network, a read-only repository and a fresh
writable output directory, twice, and both runs must produce the same
bytes. Copying a fixed file satisfies that exactly.
"""

import hashlib
import os
import shutil
import sys

# Name of the image file, both in the repository and in the output.
ENTRY_NAME = "entry.png"

# Fallback output directory when the grader does not set one. The
# grader always sets MAKEFUN_OUTPUT_DIR; this is only for local runs.
DEFAULT_OUTPUT_DIR = "out"

# Largest image the bounty allows, in bytes (1 MiB).
MAX_BYTES = 1048576


def repo_root():
    """Return the directory that holds this file (the repo root)."""
    here = os.path.abspath(__file__)
    return os.path.dirname(here)


def source_path():
    """Return the path of the shipped image inside the repository."""
    return os.path.join(repo_root(), ENTRY_NAME)


def output_dir():
    """Return the grader output directory, or the local default."""
    value = os.environ.get("MAKEFUN_OUTPUT_DIR", "")
    if value:
        return value
    return DEFAULT_OUTPUT_DIR


def output_path():
    """Return the full destination path for the copied image."""
    return os.path.join(output_dir(), ENTRY_NAME)


def sha256_of(path):
    """Return the hex sha256 digest of the file at path."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(65536)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def check_source(path):
    """Fail loudly when the shipped image is missing or too large."""
    if not os.path.isfile(path):
        raise SystemExit("missing source image: %s" % path)
    size = os.path.getsize(path)
    if size <= 0:
        raise SystemExit("source image is empty: %s" % path)
    if size > MAX_BYTES:
        raise SystemExit("source image too large: %d bytes" % size)
    return size


def copy_entry():
    """Copy entry.png into the output directory and verify the copy.

    The copy is verified byte for byte: the sha256 of the destination
    must equal the sha256 of the source, so a partial write can never
    pass silently.
    """
    src = source_path()
    size = check_source(src)
    before = sha256_of(src)
    dest = output_path()
    parent = os.path.dirname(dest)
    if parent:
        os.makedirs(parent, exist_ok=True)
    shutil.copyfile(src, dest)
    after = sha256_of(dest)
    if before != after:
        raise SystemExit("copy mismatch: %s != %s" % (before, after))
    return dest, size, after


def report(dest, size, digest):
    """Print one short line describing what was written."""
    line = "wrote %s (%d bytes, sha256 %s)" % (dest, size, digest)
    print(line)


def main():
    """Copy the image and report the result; exit non-zero on failure."""
    try:
        dest, size, digest = copy_entry()
    except OSError as exc:
        raise SystemExit("cannot write output: %s" % exc)
    report(dest, size, digest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
