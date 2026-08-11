# Build environment for cross-compiling Android SDK build-tools to
# linux-glibc-arm64.
#
# Works on x86_64 hosts. gcc-aarch64-linux-gnu cross-compiles to arm64.
#
# Base image is Debian 12 (Bookworm) - glibc 2.36, GCC 12.2
FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# Add arm64 architecture for cross-compilation libraries
RUN dpkg --add-architecture arm64

RUN apt-get update && apt-get install -y --no-install-recommends \
        bison \
        build-essential \
        ca-certificates \
        ccache \
        cmake \
        curl \
        file \
        flex \
        git \
        gnupg \
        gperf \
        gcc-aarch64-linux-gnu \
        g++-aarch64-linux-gnu \
        ninja-build \
        pkg-config \
        protobuf-compiler \
        python3 \
        python-is-python3 \
        sudo \
        unzip \
        zip \
        zlib1g-dev \
        zlib1g-dev:arm64 \
    && rm -rf /var/lib/apt/lists/*

# Non-root user
ARG USERNAME=builder
ARG USER_UID=1000
ARG USER_GID=1000

RUN if id -u 1000 >/dev/null 2>&1; then userdel -r "$(id -un 1000)" 2>/dev/null || true; fi \
    && if getent group 1000 >/dev/null 2>&1; then groupdel "$(getent group 1000 | cut -d: -f1)" 2>/dev/null || true; fi \
    && groupadd --gid ${USER_GID} ${USERNAME} \
    && useradd --uid ${USER_UID} --gid ${USER_GID} -m -s /bin/bash ${USERNAME} \
    && echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME}

USER ${USERNAME}

RUN git config --global user.name "AOSP Builder" \
    && git config --global user.email "builder@android-build-tools.local"

ENV USE_CCACHE=1 \
    CCACHE_DIR=/workspace/.ccache \
    PKG_CONFIG_LIBDIR=/usr/lib/aarch64-linux-gnu/pkgconfig:/usr/share/pkgconfig

WORKDIR /workspace
