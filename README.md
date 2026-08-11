# Android build-tools 33.0.1 for aarch64 (ARM64 Linux)

Google 官方只提供 x86_64 版本的 build-tools，不支持 ARM64 Linux。本项目提供在 ARM64 Linux 上原生运行的 build-tools 二进制文件。

## 快速开始

### 下载

从 [Releases](../../releases/tag/v33.0.1) 下载：

```bash
wget https://github.com/kmerc224/android-build-tools-aarch64/releases/download/v33.0.1/android-build-tools-33.0.1-aarch64.tar.xz
```

### 安装

```bash
# 解压
tar -xJf android-build-tools-33.0.1-aarch64.tar.xz

# 放入 Android SDK 目录
mv 33.0.1 $ANDROID_HOME/build-tools/33.0.1

# 验证
$ANDROID_HOME/build-tools/33.0.1/aapt2 version
```

### 验证完整性

```bash
sha256sum -c android-build-tools-33.0.1-aarch64.tar.xz.sha256
```

## 包含的工具

| 工具 | 架构 | 说明 |
|------|------|------|
| `aapt` | aarch64 | Android Asset Packaging Tool |
| `aapt2` | aarch64 | Android Asset Packaging Tool 2 |
| `aidl` | aarch64 | AIDL 编译器 |
| `zipalign` | aarch64 | APK 对齐工具 |
| `dexdump` | aarch64 | DEX 文件查看器 |
| `split-select` | aarch64 | APK 分割选择器 |
| `d8` | Java | DEX 编译器 |
| `apksigner` | Java | APK 签名工具 |

## 来源

基于 [AndroidIDEOfficial/androidide-tools](https://github.com/AndroidIDEOfficial/androidide-tools) 预编译的 aarch64 二进制文件，修正了 `source.properties` 中的版本号为 33.0.1。

## 许可证

MIT License
