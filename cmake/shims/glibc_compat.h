// Compatibility shim for building AOSP source with GCC + glibc
// AOSP source assumes Clang/bionic; this header bridges the gaps.

#ifndef GLIBC_COMPAT_H
#define GLIBC_COMPAT_H

#include <features.h>
#include <string.h>
#include <stdlib.h>

// AOSP uses __builtin_available() which is Clang/Apple-only
// Stub it to always return false (feature not available)
#ifndef __has_builtin
#define __has_builtin(x) 0
#endif

#ifndef __has_include
#define __has_include(x) 0
#endif

// Stub __builtin_available macro
#define __builtin_available(...) (0)

// AOSP uses C11 atomic typedef names in C++ TUs
// These are normally provided by stdatomic.h in C, but C++ needs help
#ifdef __cplusplus
#include <cstdint>
typedef _Atomic(uint8_t) atomic_uint_least8_t;
typedef _Atomic(uint16_t) atomic_uint_least16_t;
typedef _Atomic(uint32_t) atomic_uint_least32_t;
typedef _Atomic(uint64_t) atomic_uint_least64_t;
typedef _Atomic(int8_t) atomic_int_least8_t;
typedef _Atomic(int16_t) atomic_int_least16_t;
typedef _Atomic(int32_t) atomic_int_least32_t;
typedef _Atomic(int64_t) atomic_int_least64_t;
#endif

// Ensure common headers are included
#include <cstring>
#include <memory>
#include <limits>
#include <cstddef>

// GNU extensions needed
#ifndef MAP_ANONYMOUS
#define MAP_ANONYMOUS MAP_ANON
#endif

#endif // GLIBC_COMPAT_H
