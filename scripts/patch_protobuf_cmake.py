#!/usr/bin/env python3
"""Patch protobuf cmake files from cmake/ subdir to root.

In protobuf v3.19.x, CMakeLists.txt and helper .cmake/.in files live in
the cmake/ subdirectory. The key variable `protobuf_source_dir` is set via:
    get_filename_component(protobuf_source_dir ${protobuf_SOURCE_DIR} PATH)

When CMakeLists.txt was in cmake/, protobuf_SOURCE_DIR = protobuf_root/cmake/,
so protobuf_source_dir = protobuf_root. Now that we move CMakeLists.txt to
protobuf_root, protobuf_SOURCE_DIR = protobuf_root, so protobuf_source_dir
becomes the PARENT of protobuf_root (WRONG). We fix this by overriding it.
"""
import sys
from pathlib import Path


def fix_paths(text: str) -> str:
    """Fix relative paths from cmake/ context to root context."""
    # ../configure.ac was relative to cmake/ subdir; now at root
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
        # Fix the protobuf_source_dir computation.
        # Original: get_filename_component(protobuf_source_dir ${protobuf_SOURCE_DIR} PATH)
        # When CMakeLists.txt was in cmake/, PATH gave the parent = protobuf_root.
        # Now at root, PATH gives the wrong parent. Override to current dir.
        text = text.replace(
            "get_filename_component(protobuf_source_dir ${protobuf_SOURCE_DIR} PATH)",
            "set(protobuf_source_dir ${CMAKE_CURRENT_SOURCE_DIR})"
        )
        # Also fix the cmake/ reference for extract_includes.bat.in
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

    # Verify protobuf_source_dir fix
    content = root_cmakelists.read_text()
    if "set(protobuf_source_dir ${CMAKE_CURRENT_SOURCE_DIR})" in content:
        print(">>> VERIFIED: protobuf_source_dir override is present")
    else:
        print("WARNING: protobuf_source_dir override NOT found!")

    return 0


if __name__ == "__main__":
    sys.exit(main())
