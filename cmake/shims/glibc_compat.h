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

// AOSP C++ atomic type compatibility
// Clang supports _Atomic as a type qualifier in C++; GCC does not.
// Use std::atomic for GCC C++ to provide the same typedefs.
#if defined(__cplusplus) && defined(__GNUC__) && !defined(__clang__)
#include <atomic>
#include <cstdint>
typedef std::atomic<uint8_t>  atomic_uint_least8_t;
typedef std::atomic<uint16_t> atomic_uint_least16_t;
typedef std::atomic<uint32_t> atomic_uint_least32_t;
typedef std::atomic<uint64_t> atomic_uint_least64_t;
typedef std::atomic<int8_t>   atomic_int_least8_t;
typedef std::atomic<int16_t>  atomic_int_least16_t;
typedef std::atomic<int32_t>  atomic_int_least32_t;
typedef std::atomic<int64_t>  atomic_int_least64_t;
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
