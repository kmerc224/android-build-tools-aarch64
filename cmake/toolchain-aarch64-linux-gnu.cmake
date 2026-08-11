# CMake toolchain file for cross-compiling to aarch64-linux-gnu
# Used when building on x86_64 host targeting ARM64

set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR aarch64)

# Use the aarch64-linux-gnu cross-compiler
set(CMAKE_C_COMPILER aarch64-linux-gnu-gcc)
set(CMAKE_CXX_COMPILER aarch64-linux-gnu-g++)
set(CMAKE_ASM_COMPILER aarch64-linux-gnu-gcc)

# Debian/Ubuntu multiarch layout:
#   Cross-compiler:  /usr/aarch64-linux-gnu/
#   Multiarch libs:  /usr/lib/aarch64-linux-gnu/
#   Multiarch inc:   /usr/include/aarch64-linux-gnu/
#   Host includes:   /usr/include/
#
# The cross-compiler's default sysroot may not cover the multiarch
# directories, so we add them explicitly via compiler/linker flags.
set(MULTIARCH_INCLUDE /usr/include/aarch64-linux-gnu)
set(MULTIARCH_LIB /usr/lib/aarch64-linux-gnu)

# Tell the compiler about multiarch include/lib paths
add_compile_options(-isystem ${MULTIARCH_INCLUDE})
add_link_options(-L${MULTIARCH_LIB})

# CMake find_* search paths
set(CMAKE_FIND_ROOT_PATH
    /usr/aarch64-linux-gnu
    /usr/lib/aarch64-linux-gnu
    /usr/include/aarch64-linux-gnu
)

# Adjust the default behavior of the FIND_XXX() commands:
# search programs in the host environment only
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)

# search headers and libraries in the target environment
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)

# Also add to CMAKE_INCLUDE_PATH / CMAKE_LIBRARY_PATH as extra hints
# for find_path() and find_library()
list(APPEND CMAKE_INCLUDE_PATH /usr/include/aarch64-linux-gnu)
list(APPEND CMAKE_LIBRARY_PATH /usr/lib/aarch64-linux-gnu)

# pkg-config for cross-compilation
set(ENV{PKG_CONFIG_DIR} "")
set(ENV{PKG_CONFIG_LIBDIR} /usr/lib/aarch64-linux-gnu/pkgconfig:/usr/share/pkgconfig)
set(ENV{PKG_CONFIG_SYSROOT_DIR} "")

# Static linking for portability
set(BUILD_SHARED_LIBS OFF)
set(CMAKE_EXE_LINKER_FLAGS "-static-libstdc++" CACHE STRING "" FORCE)
