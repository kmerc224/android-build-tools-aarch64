# Root CMakeLists for android-build-tools-aarch64
#
# Builds Android SDK build-tools native binaries for linux-glibc-arm64.
# Source: AOSP (Android Open Source Project)
# Target: aarch64-linux-gnu (ARM64 Linux with glibc)
#
# Usage:
#   cmake -DCMAKE_TOOLCHAIN_FILE=cmake/toolchain-aarch64-linux-gnu.cmake \
#         -DPROTOC_PATH=/path/to/host-protoc \
#         -B build/linux-arm64
#   cmake --build build/linux-arm64

cmake_minimum_required(VERSION 3.18)
project(android-build-tools-aarch64)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
enable_language(ASM)

# Position-independent code required for AOSP libs
include(CheckCXXCompilerFlag)
check_cxx_compiler_flag(-fcolor-diagnostics HAVE_FCOLOR_DIAGNOSTICS)
if(HAVE_FCOLOR_DIAGNOSTICS)
    add_compile_options(-fcolor-diagnostics)
endif()

add_compile_options(-fPIC -Wno-attributes)

# Force-included compatibility header for bionic->glibc shim
add_compile_options(-include ${PROJECT_SOURCE_DIR}/cmake/shims/glibc_compat.h)

# 64-bit file offsets
add_compile_definitions(_FILE_OFFSET_BITS=64)
add_compile_definitions(_GNU_SOURCE)

# Version marker
set(TOOLS_VERSION 33.0.1)

# Source directory
set(SRC ${PROJECT_SOURCE_DIR}/src)

# ---- protoc handling ----
set(PROTOC_COMPILER)
if(DEFINED PROTOC_PATH)
    set(PROTOC_COMPILER ${PROTOC_PATH})
    if(NOT EXISTS ${PROTOC_COMPILER})
        message(FATAL_ERROR "PROTOC_PATH=${PROTOC_COMPILER} does not exist")
    endif()
    message(STATUS "Using host protoc: ${PROTOC_COMPILER}")
else()
    message(WARNING "PROTOC_PATH not set; aapt2 proto sources will not regenerate")
endif()

# ---- Third-party libraries ----
set(BUILD_SHARED_LIBS OFF CACHE BOOL "" FORCE)

# ---- Protobuf (built from source for cross-compilation) ----
# find_package(Protobuf) does not work during cross-compilation because only
# host-architecture (x86_64) libraries are installed in the Docker image.
# Instead, we build protobuf from the AOSP source tree for the target arch.
set(protobuf_BUILD_TESTS OFF CACHE BOOL "" FORCE)
set(protobuf_BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
set(protobuf_BUILD_SHARED_LIBS OFF CACHE BOOL "" FORCE)
set(protobuf_WITH_ZLIB OFF CACHE BOOL "" FORCE)
set(protobuf_ABSL_PROVIDER "module" CACHE STRING "" FORCE)

# Use the host-architecture protoc (built separately or from system package)
# for .proto code generation during the build.
if(DEFINED PROTOC_PATH)
    set(protobuf_PROTOC_EXE ${PROTOC_PATH} CACHE FILEPATH "" FORCE)
    message(STATUS "Using host protoc for protobuf codegen: ${PROTOC_PATH}")
endif()

add_subdirectory(${SRC}/abseil-cpp EXCLUDE_FROM_ALL)
add_subdirectory(${SRC}/protobuf EXCLUDE_FROM_ALL)

# Create a namespaced alias so that existing target_link_libraries() calls
# that reference protobuf::libprotobuf continue to work.
if(NOT TARGET protobuf::libprotobuf)
    if(TARGET libprotobuf)
        add_library(protobuf::libprotobuf ALIAS libprotobuf)
        message(STATUS "Using protobuf built from source (target: libprotobuf)")
    elseif(TARGET protobuf)
        add_library(protobuf::libprotobuf ALIAS protobuf)
        message(STATUS "Using protobuf built from source (target: protobuf)")
    else()
        message(FATAL_ERROR "protobuf: neither libprotobuf nor protobuf target found")
    endif()
endif()
add_subdirectory(${SRC}/fmtlib EXCLUDE_FROM_ALL)
add_subdirectory(${SRC}/pcre EXCLUDE_FROM_ALL)
add_subdirectory(${SRC}/libpng EXCLUDE_FROM_ALL)
add_subdirectory(${SRC}/expat/expat EXCLUDE_FROM_ALL)
add_subdirectory(${SRC}/boringssl EXCLUDE_FROM_ALL)
add_subdirectory(${SRC}/jsoncpp EXCLUDE_FROM_ALL)
add_subdirectory(${SRC}/zopfli EXCLUDE_FROM_ALL)
add_subdirectory(${SRC}/googletest EXCLUDE_FROM_ALL)

# ---- AOSP internal libraries + tools ----
add_subdirectory(cmake/lib)
add_subdirectory(cmake/build-tools)
