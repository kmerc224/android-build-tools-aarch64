#!/usr/bin/env python3
"""Clone the AOSP project repos listed in repos.json at a given tag.

Environment variables:
  AOSP_BRANCH   - required, a tag or branch name (e.g. platform-tools-33.0.1)
  SRC_DIR       - optional, defaults to ./src
  REPOS_JSON    - optional, defaults to ./repos.json
  JOBS          - optional, parallel clone jobs (default 4)
"""
import json
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


def log(msg: str) -> None:
    print(f">>> {msg}", flush=True)


def clone_one(repo: dict, branch: str, src_dir: Path) -> tuple:
    """Clone one repo. Returns (path, ok, message)."""
    rel_path = repo["path"]
    if rel_path.startswith("src/"):
        rel_path = rel_path[len("src/"):]
    dest = src_dir / rel_path

    if dest.is_dir() and (dest / ".git").exists():
        want = subprocess.run(
            ["git", "rev-parse", "--verify", f"refs/tags/{branch}^{{commit}}"],
            cwd=dest, capture_output=True, text=True,
        )
        have = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=dest, capture_output=True, text=True,
        )
        if want.returncode == 0 and have.returncode == 0 \
                and want.stdout.strip() == have.stdout.strip():
            return (str(dest), True, "already cloned (ref matches)")
        shutil.rmtree(dest)

    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(
            [
                "git", "clone",
                "-c", "advice.detachedHead=false",
                "--depth", "1",
                "--branch", branch,
                repo["url"],
                str(dest),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        return (str(dest), True, "cloned")
    except subprocess.CalledProcessError as e:
        return (str(dest), False, e.stderr.strip().split("\n")[-1])


def install_shims(src_dir: Path, patch_dir: Path) -> None:
    """Drop pre-generated source files into the cloned tree."""
    misc = patch_dir / "misc"
    if not misc.is_dir():
        return

    drops = [
        ("IncrementalProperties.sysprop.h",
         "incremental_delivery/sysprop/include/IncrementalProperties.sysprop.h"),
        ("IncrementalProperties.sysprop.cpp",
         "incremental_delivery/sysprop/IncrementalProperties.sysprop.cpp"),
        ("platform_tools_version.h",
         "soong/cc/libbuildversion/include/platform_tools_version.h"),
    ]

    log("installing pre-generated source shims")
    for filename, rel_dest in drops:
        srcfile = misc / filename
        dest = src_dir / rel_dest
        if not srcfile.is_file():
            print(f"  !! missing source: {srcfile}")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(srcfile, dest)
        print(f"  installed {filename} -> {rel_dest}")


def link_protobuf_submodules(src_dir: Path) -> None:
    """Link abseil-cpp into protobuf's third_party directory."""
    protobuf = src_dir / "protobuf"
    abseil = src_dir / "abseil-cpp"
    if not protobuf.is_dir() or not abseil.is_dir():
        return

    target = protobuf / "third_party" / "abseil-cpp"
    if target.exists() or target.is_symlink():
        return

    target.parent.mkdir(parents=True, exist_ok=True)
    target.symlink_to(Path("../../abseil-cpp"))
    log(f"linked {target.relative_to(src_dir)} -> ../../abseil-cpp")


def fix_aapt2_proto_paths(src_dir: Path) -> None:
    """Fix aapt2's .proto file import paths."""
    aapt2_dir = src_dir / "base" / "tools" / "aapt2"
    if not aapt2_dir.is_dir():
        return

    replacements = {
        "frameworks/base/tools/aapt2/Configuration.proto": "Configuration.proto",
        "frameworks/base/tools/aapt2/Resources.proto": "Resources.proto",
    }

    touched = []
    for proto in aapt2_dir.glob("*.proto"):
        text = proto.read_text()
        new = text
        for old, repl in replacements.items():
            new = new.replace(old, repl)
        if new != text:
            proto.write_text(new)
            touched.append(proto.name)

    if touched:
        log(f"rewrote proto import paths in: {', '.join(touched)}")


def main() -> int:
    branch = os.environ.get("AOSP_BRANCH")
    if not branch:
        sys.exit("error: AOSP_BRANCH must be set (e.g. platform-tools-33.0.1)")

    src_dir = Path(os.environ.get("SRC_DIR", "./src"))
    repos_json = Path(os.environ.get("REPOS_JSON", "./repos.json"))
    patch_dir = Path(os.environ.get("PATCH_DIR", "./patches"))
    jobs = int(os.environ.get("JOBS") or 4)

    with repos_json.open() as f:
        repos = json.load(f)

    src_dir.mkdir(parents=True, exist_ok=True)
    log(f"cloning {len(repos)} repos at {branch} into {src_dir} ({jobs} parallel)")

    failures = []
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        futures = {pool.submit(clone_one, r, branch, src_dir): r for r in repos}
        for fut in as_completed(futures):
            dest, ok, msg = fut.result()
            marker = "ok " if ok else "FAIL"
            print(f"  [{marker}] {dest}: {msg}", flush=True)
            if not ok:
                failures.append((dest, msg))

    if failures:
        log(f"{len(failures)} clone(s) failed:")
        for dest, msg in failures:
            print(f"  {dest}: {msg}")
        return 1

    install_shims(src_dir, patch_dir)
    link_protobuf_submodules(src_dir)
    fix_aapt2_proto_paths(src_dir)

    size = subprocess.check_output(
        ["du", "-sh", str(src_dir)], text=True
    ).split()[0]
    log(f"sources ready: {size} on disk")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
