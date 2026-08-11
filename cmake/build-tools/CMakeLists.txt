# Build tools executables

# aapt - Android Asset Packaging Tool (legacy)
add_executable(aapt
    ${SRC}/base/tools/aapt/AaptAssets.cpp
    ${SRC}/base/tools/aapt/AaptConfig.cpp
    ${SRC}/base/tools/aapt/AaptUtil.cpp
    ${SRC}/base/tools/aapt/AaptXml.cpp
    ${SRC}/base/tools/aapt/ApkBuilder.cpp
    ${SRC}/base/tools/aapt/Command.cpp
    ${SRC}/base/tools/aapt/CrunchCache.cpp
    ${SRC}/base/tools/aapt/FileGroup.cpp
    ${SRC}/base/tools/aapt/Images.cpp
    ${SRC}/base/tools/aapt/Package.cpp
    ${SRC}/base/tools/aapt/pseudolocalize.cpp
    ${SRC}/base/tools/aapt/Resource.cpp
    ${SRC}/base/tools/aapt/ResourceFilter.cpp
    ${SRC}/base/tools/aapt/ResourceIdCache.cpp
    ${SRC}/base/tools/aapt/ResourceTable.cpp
    ${SRC}/base/tools/aapt/SplitParams.cpp
    ${SRC}/base/tools/aapt/StringPool.cpp
    ${SRC}/base/tools/aapt/WorkQueue.cpp
    ${SRC}/base/tools/aapt/XmlFlattener.cpp
    ${SRC}/base/tools/aapt/Main.cpp
)
target_include_directories(aapt PRIVATE
    ${SRC}/base/tools/aapt
    ${SRC}/base/tools/aapt2
    ${SRC}/base/libs/androidfw/include
    ${SRC}/core/libutils/include
    ${SRC}/core/liblog/include
    ${SRC}/core/libcutils/include
    ${SRC}/core/libziparchive/include
    ${SRC}/core/include
    ${SRC}/native/include
    ${SRC}/libpng
    ${SRC}/expat/lib
    ${SRC}/jsoncpp/include
    ${SRC}/zopfli/src
)
target_link_libraries(aapt PRIVATE
    androidfw utils log cutils ziparchive buildversion
    png expat z jsoncpp
    protobuf::libprotobuf
)

# aapt2 - Android Asset Packaging Tool 2
add_executable(aapt2
    ${SRC}/base/tools/aapt2/compile/Compile.cpp
    ${SRC}/base/tools/aapt2/compile/IdAssigner.cpp
    ${SRC}/base/tools/aapt2/compile/PngChunkFilter.cpp
    ${SRC}/base/tools/aapt2/compile/PngCrunch.cpp
    ${SRC}/base/tools/aapt2/decompress/Decompress.cpp
    ${SRC}/base/tools/aapt2/dump/DumpManifest.cpp
    ${SRC}/base/tools/aapt2/filter/AbiFilter.cpp
    ${SRC}/base/tools/aapt2/filter/ConfigFilter.cpp
    ${SRC}/base/tools/aapt2/format/Archive.cpp
    ${SRC}/base/tools/aapt2/format/Container.cpp
    ${SRC}/base/tools/aapt2/format/binary/BinaryResourceParser.cpp
    ${SRC}/base/tools/aapt2/format/binary/ResChunkPullParser.cpp
    ${SRC}/base/tools/aapt2/format/binary/XmlFlattener.cpp
    ${SRC}/base/tools/aapt2/format/proto/ProtoDeserialize.cpp
    ${SRC}/base/tools/aapt2/format/proto/ProtoSerialize.cpp
    ${SRC}/base/tools/aapt2/io/BigBufferStream.cpp
    ${SRC}/base/tools/aapt2/io/File.cpp
    ${SRC}/base/tools/aapt2/io/FileStream.cpp
    ${SRC}/base/tools/aapt2/io/StringStream.cpp
    ${SRC}/base/tools/aapt2/io/Util.cpp
    ${SRC}/base/tools/aapt2/io/ZipArchive.cpp
    ${SRC}/base/tools/aapt2/link/AutoAddOverlay.cpp
    ${SRC}/base/tools/aapt2/link/FlagDuplicatedResources.cpp
    ${SRC}/base/tools/aapt2/link/Link.cpp
    ${SRC}/base/tools/aapt2/link/ManifestFixer.cpp
    ${SRC}/base/tools/aapt2/link/NoDefaultResourceRemover.cpp
    ${SRC}/base/tools/aapt2/link/OverlayableCheck.cpp
    ${SRC}/base/tools/aapt2/link/PrivateAttributeMover.cpp
    ${SRC}/base/tools/aapt2/link/ReferenceLinker.cpp
    ${SRC}/base/tools/aapt2/link/ResourceExcluder.cpp
    ${SRC}/base/tools/aapt2/link/TableMerger.cpp
    ${SRC}/base/tools/aapt2/optimize/MultiApkOptimizer.cpp
    ${SRC}/base/tools/aapt2/optimize/Obfuscator.cpp
    ${SRC}/base/tools/aapt2/optimize/ResourceDeduper.cpp
    ${SRC}/base/tools/aapt2/optimize/VersionCollapser.cpp
    ${SRC}/base/tools/aapt2/process/SymbolTable.cpp
    ${SRC}/base/tools/aapt2/split/TableSplitter.cpp
    ${SRC}/base/tools/aapt2/text/Printer.cpp
    ${SRC}/base/tools/aapt2/text/Unicode.cpp
    ${SRC}/base/tools/aapt2/text/Utf8Iterator.cpp
    ${SRC}/base/tools/aapt2/util/Files.cpp
    ${SRC}/base/tools/aapt2/util/Util.cpp
    ${SRC}/base/tools/aapt2/Debug.cpp
    ${SRC}/base/tools/aapt2/DominatorTree.cpp
    ${SRC}/base/tools/aapt2/LoadedApk.cpp
    ${SRC}/base/tools/aapt2/Resource.cpp
    ${SRC}/base/tools/aapt2/ResourceParser.cpp
    ${SRC}/base/tools/aapt2/ResourceTable.cpp
    ${SRC}/base/tools/aapt2/ResourceUtils.cpp
    ${SRC}/base/tools/aapt2/ResourceValues.cpp
    ${SRC}/base/tools/aapt2/SdkConstants.cpp
    ${SRC}/base/tools/aapt2/StringPool.cpp
    ${SRC}/base/tools/aapt2/trace/TraceBuffer.cpp
    ${SRC}/base/tools/aapt2/xml/XmlActionExecutor.cpp
    ${SRC}/base/tools/aapt2/xml/XmlDom.cpp
    ${SRC}/base/tools/aapt2/xml/XmlPullParser.cpp
    ${SRC}/base/tools/aapt2/xml/XmlUtil.cpp
    ${SRC}/base/tools/aapt2/Tool.cpp
    ${SRC}/base/tools/aapt2/ValueTransformer.cpp
)
target_include_directories(aapt2 PRIVATE
    ${SRC}/base/tools/aapt2
    ${SRC}/base/libs/androidfw/include
    ${SRC}/core/libutils/include
    ${SRC}/core/liblog/include
    ${SRC}/core/libcutils/include
    ${SRC}/core/libziparchive/include
    ${SRC}/core/include
    ${SRC}/native/include
    ${SRC}/libpng
    ${SRC}/expat/lib
    ${SRC}/protobuf/src
    ${SRC}/abseil-cpp
)
target_link_libraries(aapt2 PRIVATE
    androidfw utils log cutils ziparchive buildversion
    png expat
    protobuf::libprotobuf
    absl::strings
    absl::str_format
    fmt
)

# aidl - Android Interface Definition Language compiler
add_executable(aidl
    ${SRC}/aidl/aidl_checkapi.cpp
    ${SRC}/aidl/aidl_const.cpp
    ${SRC}/aidl/aidl_to_common.cpp
    ${SRC}/aidl/aidl_to_cpp_common.cpp
    ${SRC}/aidl/aidl_to_cpp.cpp
    ${SRC}/aidl/aidl_to_java.cpp
    ${SRC}/aidl/aidl_to_ndk.cpp
    ${SRC}/aidl/aidl_to_rust.cpp
    ${SRC}/aidl/aidl_typenames.cpp
    ${SRC}/aidl/aidl.cpp
    ${SRC}/aidl/ast_java.cpp
    ${SRC}/aidl/check_valid.cpp
    ${SRC}/aidl/code_writer.cpp
    ${SRC}/aidl/constant_expression.cpp
    ${SRC}/aidl/diagnostics.cpp
    ${SRC}/aidl/generate_aidl_mappings.cpp
    ${SRC}/aidl/generate_cpp.cpp
    ${SRC}/aidl/generate_cpp_analyzer.cpp
    ${SRC}/aidl/generate_cpp_const.cpp
    ${SRC}/aidl/generate_cpp_enum.cpp
    ${SRC}/aidl/generate_cpp_parcelable.cpp
    ${SRC}/aidl/generate_cpp_union.cpp
    ${SRC}/aidl/generate_java.cpp
    ${SRC}/aidl/generate_java_binder.cpp
    ${SRC}/aidl/generate_java_const.cpp
    ${SRC}/aidl/generate_java_enum.cpp
    ${SRC}/aidl/generate_java_parcelable.cpp
    ${SRC}/aidl/generate_java_union.cpp
    ${SRC}/aidl/generate_ndk.cpp
    ${SRC}/aidl/generate_ndk_aidl.cpp
    ${SRC}/aidl/generate_ndk_backed.cpp
    ${SRC}/aidl/generate_ndk_cpp.cpp
    ${SRC}/aidl/generate_ndk_java.cpp
    ${SRC}/aidl/generate_ndk_rust.cpp
    ${SRC}/aidl/generate_rust.cpp
    ${SRC}/aidl/generate_rust_const.cpp
    ${SRC}/aidl/generate_rust_enum.cpp
    ${SRC}/aidl/generate_rust_parcelable.cpp
    ${SRC}/aidl/generate_rust_union.cpp
    ${SRC}/aidl/import_resolver.cpp
    ${SRC}/aidl/io_delegate.cpp
    ${SRC}/aidl/language.cpp
    ${SRC}/aidl/lexer.cpp
    ${SRC}/aidl/logging.cpp
    ${SRC}/aidl/main.cpp
    ${SRC}/aidl/metrics.cpp
    ${SRC}/aidl/option.cpp
    ${SRC}/aidl/parser.cpp
    ${SRC}/aidl/permission.cpp
    ${SRC}/aidl/preprocessor.cpp
    ${SRC}/aidl/type.cpp
)
target_include_directories(aidl PRIVATE
    ${SRC}/aidl
    ${SRC}/aidl/include
    ${SRC}/base/libs/androidfw/include
    ${SRC}/core/libutils/include
    ${SRC}/core/liblog/include
    ${SRC}/core/libcutils/include
    ${SRC}/core/include
    ${SRC}/native/include
    ${SRC}/fmtlib/include
    ${SRC}/googletest/googlemock/include
)
target_link_libraries(aidl PRIVATE
    utils log cutils
    fmt
    gmock
)

# zipalign - ZIP alignment tool
add_executable(zipalign
    ${SRC}/build/tools/zipalign/ZipAlign.cpp
    ${SRC}/build/tools/zipalign/ZipEntry.cpp
    ${SRC}/build/tools/zipalign/ZipFile.cpp
    ${SRC}/core/libutils/BackupData.cpp
    ${SRC}/core/libziparchive/zip_archive.cc
    ${SRC}/core/libziparchive/zip_archive_stream_entry.cc
    ${SRC}/core/libziparchive/zip_cd_entry_map.cc
    ${SRC}/core/libziparchive/zip_error.cpp
    ${SRC}/core/libziparchive/zip_writer.cc
)
target_include_directories(zipalign PRIVATE
    ${SRC}/build/tools/zipalign
    ${SRC}/core/libutils/include
    ${SRC}/core/libziparchive/include
    ${SRC}/core/liblog/include
    ${SRC}/core/libcutils/include
    ${SRC}/core/include
    ${SRC}/zopfli/src
)
target_link_libraries(zipalign PRIVATE
    log cutils z zopfli
)

# dexdump - DEX file dumper
add_executable(dexdump
    ${SRC}/dalvik/tools/dexdump/dexdump.cpp
    ${SRC}/dalvik/tools/dexdump/dexdump_cfg.cpp
)
target_include_directories(dexdump PRIVATE
    ${SRC}/dalvik/tools/dexdump
    ${SRC}/dalvik/libdex
    ${SRC}/core/libutils/include
    ${SRC}/core/liblog/include
    ${SRC}/core/include
)
target_link_libraries(dexdump PRIVATE
    log utils
)

# split-select - APK split selector
add_executable(split-select
    ${SRC}/base/tools/split-select/Abi.cpp
    ${SRC}/base/tools/split-select/Density.cpp
    ${SRC}/base/tools/split-select/Group.cpp
    ${SRC}/base/tools/split-select/Rule.cpp
    ${SRC}/base/tools/split-select/RuleGenerator.cpp
    ${SRC}/base/tools/split-select/SplitDescription.cpp
    ${SRC}/base/tools/split-select/SplitSelector.cpp
    ${SRC}/base/tools/split-select/Main.cpp
)
target_include_directories(split-select PRIVATE
    ${SRC}/base/tools/split-select
    ${SRC}/base/libs/androidfw/include
    ${SRC}/core/libutils/include
    ${SRC}/core/liblog/include
    ${SRC}/core/libcutils/include
    ${SRC}/core/include
    ${SRC}/jsoncpp/include
)
target_link_libraries(split-select PRIVATE
    androidfw utils log cutils jsoncpp
)
