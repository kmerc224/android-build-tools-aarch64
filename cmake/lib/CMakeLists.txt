# AOSP internal libraries needed by build-tools

# libbase - base utility library
add_library(libbase STATIC
    ${SRC}/libbase/abi_compatibility.cpp
    ${SRC}/libbase/chrono_utils.cpp
    ${SRC}/libbase/cmsg.cpp
    ${SRC}/libbase/errors.cpp
    ${SRC}/libbase/file.cpp
    ${SRC}/libbase/hex.cpp
    ${SRC}/libbase/logging.cpp
    ${SRC}/libbase/mapped_file.cpp
    ${SRC}/libbase/parsebool.cpp
    ${SRC}/libbase/parsenetaddress.cpp
    ${SRC}/libbase/posix_strerror_r.cpp
    ${SRC}/libbase/process.cpp
    ${SRC}/libbase/properties.cpp
    ${SRC}/libbase/string.cpp
    ${SRC}/libbase/strings.cpp
    ${SRC}/libbase/threads.cpp
)
target_include_directories(libbase PUBLIC
    ${SRC}/libbase/include
    ${SRC}/core/include
)
target_link_libraries(libbase PUBLIC log)

# liblog - Android logging
add_library(log STATIC
    ${SRC}/core/liblog/log_event_list.cpp
    ${SRC}/core/liblog/log_event_write.cpp
    ${SRC}/core/liblog/logger_name.cpp
    ${SRC}/core/liblog/logger_read.cpp
    ${SRC}/core/liblog/logger_write.cpp
    ${SRC}/core/liblog/properties.cpp
    ${SRC}/core/liblog/logprint.cpp
)
target_include_directories(log PUBLIC
    ${SRC}/core/liblog/include
    ${SRC}/logging/liblog/include
    ${SRC}/core/include
)
target_compile_definitions(log PRIVATE
    LIBLOG_LOG_TAG=1006
    _REALLY_ALLOW_NON_MOVABLE_STDATOMIC_FOR_ANDROID_LOGGING
)

# libcutils - C utility functions
add_library(cutils STATIC
    ${SRC}/core/libcutils/android_get_control_file.cpp
    ${SRC}/core/libcutils/ashmem_host.cpp
    ${SRC}/core/libcutils/config_utils.cpp
    ${SRC}/core/libcutils/fs.cpp
    ${SRC}/core/libcutils/hashmap.cpp
    ${SRC}/core/libcutils/iosched_policy.cpp
    ${SRC}/core/libcutils/load_file.cpp
    ${SRC}/core/libcutils/multiuser.cpp
    ${SRC}/core/libcutils/native_handle.cpp
    ${SRC}/core/libcutils/properties.cpp
    ${SRC}/core/libcutils/record_stream.cpp
    ${SRC}/core/libcutils/socket_inaddr_any_server.cpp
    ${SRC}/core/libcutils/socket_local_client.cpp
    ${SRC}/core/libcutils/socket_local_server.cpp
    ${SRC}/core/libcutils/socket_network_client.cpp
    ${SRC}/core/libcutils/sockets.cpp
    ${SRC}/core/libcutils/str_parms.cpp
    ${SRC}/core/libcutils/trace.cpp
)
target_include_directories(cutils PUBLIC
    ${SRC}/core/libcutils/include
    ${SRC}/core/include
)
target_compile_definitions(cutils PRIVATE
    _GNU_SOURCE
)
target_link_libraries(cutils PUBLIC log)

# libutils - Android utility classes
add_library(utils STATIC
    ${SRC}/core/libutils/FileMap.cpp
    ${SRC}/core/libutils/Looper.cpp
    ${SRC}/core/libutils/NativeHandle.cpp
    ${SRC}/core/libutils/Printer.cpp
    ${SRC}/core/libutils/StopWatch.cpp
    ${SRC}/core/libutils/SystemClock.cpp
    ${SRC}/core/libutils/Threads.cpp
    ${SRC}/core/libutils/Timers.cpp
    ${SRC}/core/libutils/Tokenizer.cpp
    ${SRC}/core/libutils/SharedBuffer.cpp
    ${SRC}/core/libutils/String8.cpp
    ${SRC}/core/libutils/String16.cpp
    ${SRC}/core/libutils/VectorImpl.cpp
    ${SRC}/core/libutils/RefBase.cpp
    ${SRC}/core/libutils/Unicode.cpp
)
target_include_directories(utils PUBLIC
    ${SRC}/core/libutils/include
    ${SRC}/core/libsystem/include
    ${SRC}/core/include
    ${SRC}/native/include
)
target_link_libraries(utils PUBLIC cutils log)

# libandroidfw - Android framework library
add_library(androidfw STATIC
    ${SRC}/base/libs/androidfw/ApkAssets.cpp
    ${SRC}/base/libs/androidfw/Asset.cpp
    ${SRC}/base/libs/androidfw/AssetDir.cpp
    ${SRC}/base/libs/androidfw/AssetManager.cpp
    ${SRC}/base/libs/androidfw/AssetManager2.cpp
    ${SRC}/base/libs/androidfw/AttributeResolution.cpp
    ${SRC}/base/libs/androidfw/Chunk_iterator.cpp
    ${SRC}/base/libs/androidfw/ConfigDescription.cpp
    ${SRC}/base/libs/androidfw/Idmap.cpp
    ${SRC}/base/libs/androidfw/LoadedArsc.cpp
    ${SRC}/base/libs/androidfw/Locale.cpp
    ${SRC}/base/libs/androidfw/LocaleData.cpp
    ${SRC}/base/libs/androidfw/ObbFile.cpp
    ${SRC}/base/libs/androidfw/ResourceTypes.cpp
    ${SRC}/base/libs/androidfw/ResourceUtils.cpp
    ${SRC}/base/libs/androidfw/StreamingZipInflater.cpp
    ${SRC}/base/libs/androidfw/TypeWrappers.cpp
    ${SRC}/base/libs/androidfw/Util.cpp
    ${SRC}/base/libs/androidfw/ZipUtils.cpp
)
target_include_directories(androidfw PUBLIC
    ${SRC}/base/libs/androidfw/include
    ${SRC}/base/cmds/libandroidfw/include
    ${SRC}/core/libutils/include
    ${SRC}/core/liblog/include
    ${SRC}/core/include
    ${SRC}/native/include
)
target_link_libraries(androidfw PUBLIC utils log cutils base)

# libziparchive
add_library(ziparchive STATIC
    ${SRC}/core/libziparchive/zip_archive.cc
    ${SRC}/core/libziparchive/zip_archive_stream_entry.cc
    ${SRC}/core/libziparchive/zip_cd_entry_map.cc
    ${SRC}/core/libziparchive/zip_error.cpp
    ${SRC}/core/libziparchive/zip_writer.cc
)
target_include_directories(ziparchive PUBLIC
    ${SRC}/core/libziparchive/include
    ${SRC}/core/include
)
target_link_libraries(ziparchive PUBLIC base log)

# libbuildversion
add_library(buildversion STATIC
    ${SRC}/soong/cc/libbuildversion/libbuildversion.cpp
)
target_include_directories(buildversion PUBLIC
    ${SRC}/soong/cc/libbuildversion/include
)

# libpackagelistparser
add_library(packagelistparser STATIC
    ${SRC}/core/libpackagelistparser/packagelistparser.cpp
)
target_include_directories(packagelistparser PUBLIC
    ${SRC}/core/libpackagelistparser/include
    ${SRC}/core/libcutils/include
    ${SRC}/logging/liblog/include
)
target_link_libraries(packagelistparser PUBLIC log)
