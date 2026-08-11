#!/usr/bin/env python3
"""Build Android build-tools for linux-arm64.

This script:
1. Builds host protoc (needed for generating protobuf code)
2. Cross-compiles all build-tools for aarch64-linux-gnu

Environment variables:
  SRC_DIR      - source directory (default: ./src)
  BUILD_DIR    - build directory (default: ./build/linux-arm64)
  PROTOC_PATH  - path to host protoc binary (optional, will build if not set)
  JOBS         - parallel build jobs (default: nproc)
"""
import os
import subprocess
import sys
from pathlib import Path


def log(msg: str) -> None:
    print(f">>> {msg}", flush=True)


def build_host_protoc(src_dir: Path, build_dir: Path) -> Path:
    """Build protoc for the host architecture."""
    protoc_build = build_dir / "host-protoc"
    protoc = protoc_build / "protoc"

    if protoc.exists():
        log(f"host protoc already built: {protoc}")
        return protoc

    log("building host protoc...")
    protoc_build.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [
            "cmake",
            "-S", str(src_dir / "protobuf"),
            "-B", str(protoc_build),
            "-GNinja",
            "-Dprotobuf_BUILD_TESTS=OFF",
            "-Dprotobuf_BUILD_EXAMPLES=OFF",
        ],
        check=True,
    )
    subprocess.run(
        ["ninja", "-C", str(protoc_build), "protoc"],
        check=True,
    )

    log(f"host protoc built: {protoc}")
    return protoc


def build_target(src_dir: Path, build_dir: Path, protoc: Path) -> None:
    """Cross-compile build-tools for aarch64-linux-gnu."""
    project_dir = Path(__file__).parent.parent
    toolchain = project_dir / "cmake" / "toolchain-aarch64-linux-gnu.cmake"

    log(f"configuring target build in {build_dir}...")
    build_dir.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [
            "cmake",
            "-S", str(project_dir),
            "-B", str(build_dir),
            "-GNinja",
            f"-DCMAKE_TOOLCHAIN_FILE={toolchain}",
            f"-DPROTOC_PATH={protoc}",
        ],
        check=True,
    )

    jobs = int(os.environ.get("JOBS") or os.cpu_count() or 4)
    log(f"building target with {jobs} jobs...")
    subprocess.run(
        ["ninja", "-C", str(build_dir), "-j", str(jobs)],
        check=True,
    )

    log("target build complete!")


def collect_artifacts(build_dir: Path, output_dir: Path, version: str) -> None:
    """Collect built binaries into output directory."""
    tools = ["aapt", "aapt2", "aidl", "zipalign", "dexdump", "split-select"]

    output_dir.mkdir(parents=True, exist_ok=True)

    for tool in tools:
        src = build_dir / tool
        if src.exists():
            dst = output_dir / tool
            subprocess.run(["cp", str(src), str(dst)], check=True)
            subprocess.run(["chmod", "+x", str(dst)], check=True)
            log(f"copied {tool} -> {dst}")

    # Create source.properties
    props = output_dir / "source.properties"
    props.write_text(f"""Pkg.UserSrc=true
Pkg.Revision={version}
""")
    log(f"created {props}")


def main() -> int:
    src_dir = Path(os.environ.get("SRC_DIR", "./src"))
    build_dir = Path(os.environ.get("BUILD_DIR", "./build/linux-arm64"))
    output_dir = Path(os.environ.get("OUTPUT_DIR", "./out/linux-arm64"))
    version = os.environ.get("BUILD_TOOLS_LABEL", "33.0.1")

    if not src_dir.is_dir():
        sys.exit(f"error: source directory not found: {src_dir}")

    # Build host protoc
    protoc_path = os.environ.get("PROTOC_PATH")
    if protoc_path:
        protoc = Path(protoc_path)
    else:
        protoc = build_host_protoc(src_dir, build_dir.parent / "host-protoc")

    # Build target
    build_target(src_dir, build_dir, protoc)

    # Collect artifacts
    collect_artifacts(build_dir, output_dir, version)

    log(f"artifacts collected in {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
