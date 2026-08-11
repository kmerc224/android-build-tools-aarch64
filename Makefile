# Makefile for building Android build-tools for aarch64
#
# Usage:
#   make linux-arm64                    # Full build
#   make fetch                          # Just fetch sources
#   make image-linux-arm64              # Just build Docker image
#   make shell-linux-arm64              # Drop into build container
#   make clean                          # Remove build outputs
#   make distclean                      # Remove everything including sources

.PHONY: help linux-arm64 image-linux-arm64 fetch build shell-linux-arm64 clean distclean

# Load configuration
-include config.env

# Defaults
AOSP_BRANCH ?= platform-tools-33.0.1
BUILD_TOOLS_LABEL ?= 33.0.1
TARGETS ?= aapt aapt2 aidl zipalign dexdump split-select
JOBS ?= $(shell nproc)
CCACHE_DIR ?= ./.ccache

# Directories
SRC_DIR := ./src
BUILD_DIR := ./build/linux-arm64
OUTPUT_DIR := ./out/linux-arm64
DOCKER_IMAGE := android-build-tools

help:
	@echo "Android build-tools aarch64 builder"
	@echo ""
	@echo "Targets:"
	@echo "  linux-arm64       - Full build (image + fetch + build)"
	@echo "  image-linux-arm64 - Build Docker image only"
	@echo "  fetch             - Fetch AOSP sources only"
	@echo "  build             - Build tools only (requires sources)"
	@echo "  shell-linux-arm64 - Open shell in build container"
	@echo "  clean             - Remove build outputs"
	@echo "  distclean         - Remove everything including sources"
	@echo ""
	@echo "Configuration (from config.env or environment):"
	@echo "  AOSP_BRANCH       = $(AOSP_BRANCH)"
	@echo "  BUILD_TOOLS_LABEL = $(BUILD_TOOLS_LABEL)"
	@echo "  TARGETS           = $(TARGETS)"
	@echo "  JOBS              = $(JOBS)"

linux-arm64: image-linux-arm64 fetch build

image-linux-arm64:
	docker build \
		-t $(DOCKER_IMAGE) \
		-f docker/linux-arm64.Dockerfile \
		.

fetch:
	@mkdir -p $(SRC_DIR)
	docker run --rm \
		-v $(CURDIR):/workspace \
		-w /workspace \
		-e AOSP_BRANCH=$(AOSP_BRANCH) \
		-e SRC_DIR=/workspace/$(SRC_DIR) \
		-e REPOS_JSON=/workspace/repos.json \
		-e PATCH_DIR=/workspace/patches \
		-e JOBS=$(JOBS) \
		$(DOCKER_IMAGE) \
		python3 scripts/fetch_sources.py

build:
	@mkdir -p $(BUILD_DIR) $(OUTPUT_DIR)
	# Build host protoc first
	docker run --rm \
		-v $(CURDIR):/workspace \
		-w /workspace \
		$(DOCKER_IMAGE) \
		bash -c "mkdir -p build/host-protoc && \
			cmake -S src/protobuf -B build/host-protoc -GNinja \
				-Dprotobuf_BUILD_TESTS=OFF \
				-Dprotobuf_BUILD_EXAMPLES=OFF && \
			ninja -C build/host-protoc protoc"
	# Build target tools
	docker run --rm \
		-v $(CURDIR):/workspace \
		-w /workspace \
		-e SRC_DIR=/workspace/$(SRC_DIR) \
		-e BUILD_DIR=/workspace/$(BUILD_DIR) \
		-e OUTPUT_DIR=/workspace/$(OUTPUT_DIR) \
		-e BUILD_TOOLS_LABEL=$(BUILD_TOOLS_LABEL) \
		-e JOBS=$(JOBS) \
		$(DOCKER_IMAGE) \
		python3 scripts/build_linux_arm64.py

shell-linux-arm64:
	docker run --rm -it \
		-v $(CURDIR):/workspace \
		-w /workspace \
		$(DOCKER_IMAGE) \
		bash

clean:
	rm -rf build out

distclean: clean
	rm -rf src .ccache

# Verify built binaries
verify:
	@echo "=== Checking binary architectures ==="
	@for tool in $(TARGETS); do \
		if [ -f "$(OUTPUT_DIR)/$$tool" ]; then \
			echo "--- $$tool ---"; \
			file $(OUTPUT_DIR)/$$tool; \
		else \
			echo "WARNING: $$tool not found"; \
		fi \
	done
	@echo ""
	@echo "=== source.properties ==="
	@cat $(OUTPUT_DIR)/source.properties 2>/dev/null || echo "Not found"

# Create release archive
archive:
	@mkdir -p dist
	cd $(OUTPUT_DIR) && \
		tar -cJf ../../dist/android-build-tools-$(BUILD_TOOLS_LABEL)-aarch64.tar.xz \
			$(TARGETS) source.properties
	cd dist && \
		sha256sum android-build-tools-$(BUILD_TOOLS_LABEL)-aarch64.tar.xz \
			> android-build-tools-$(BUILD_TOOLS_LABEL)-aarch64.tar.xz.sha256
	@echo ""
	@echo "Archive created: dist/android-build-tools-$(BUILD_TOOLS_LABEL)-aarch64.tar.xz"
