#!/usr/bin/env python3
"""Patch protobuf cmake files from cmake/ subdir to root.

In protobuf v3.19.x, CMakeLists.txt and helper .cmake/.in files live in
the cmake/ subdirectory with relative paths (../src, ../configure.ac)
designed for that location. This script copies them to the protobuf root
and fixes paths so add_subdirectory(src/protobuf) works.

This runs on the HOST (not inside Docker) to ensure files are visible
to subsequent build steps via bind mounts.
"""
import sys
from pathlib import Path


def fix_paths(text: str) -> str:
    """Fix relative paths from cmake/ context to root context."""
    text = text.replace("${CMAKE_CURRENT_SOURCE_DIR}/../src",
                        "${CMAKE_CURRENT_SOURCE_DIR}/src")
    text = text.replace('"../src', '"${CMAKE_CURRENT_SOURCE_DIR}/src')
    text = text.replace("../configure.ac", "configure.ac")
    return text


def main() -> int:
    protobuf_dir = Path("src/protobuf")
    cmake_subdir = protobuf_dir / "cmake"

    if not cmake_subdir.is_dir():
        print(f"ERROR: {cmake_subdir} not found")
        return 1

    patched = 0

    # Copy and patch CMakeLists.txt
    cmakelists = cmake_subdir / "CMakeLists.txt"
    if cmakelists.exists():
        text = fix_paths(cmakelists.read_text())
        text = text.replace("${CMAKE_CURRENT_SOURCE_DIR}/../cmake",
                            "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
        (protobuf_dir / "CMakeLists.txt").write_text(text)
        patched += 1

    # Copy and patch all .cmake helper files
    for f in cmake_subdir.glob("*.cmake"):
        text = fix_paths(f.read_text())
        (protobuf_dir / f.name).write_text(text)
        patched += 1

    # Copy .in template files
    for f in cmake_subdir.glob("*.in"):
        dst = protobuf_dir / f.name
        text = fix_paths(f.read_text())
        dst.write_text(text)
        patched += 1

    print(f">>> patched {patched} protobuf cmake files from cmake/ to root")

    # Verify critical files exist
    root_cmakelists = protobuf_dir / "CMakeLists.txt"
    if not root_cmakelists.exists():
        print("ERROR: CMakeLists.txt was not created at protobuf root!")
        return 1
    print(f">>> VERIFIED: {root_cmakelists} exists ({root_cmakelists.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
