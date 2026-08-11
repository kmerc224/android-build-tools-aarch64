# Android build-tools for aarch64

从 AOSP 源码编译 Android SDK build-tools 的 ARM64 (aarch64) 版本。

## 背景

Google 官方只提供 x86_64 版本的 build-tools，不支持 ARM64 Linux。本项目从 AOSP 源码编译，生成可在 ARM64 Linux 上运行的原生二进制文件。

## 支持的工具

| 工具 | 说明 |
|------|------|
| `aapt` | Android Asset Packaging Tool (旧版) |
| `aapt2` | Android Asset Packaging Tool 2 |
| `aidl` | Android Interface Definition Language 编译器 |
| `zipalign` | APK 对齐工具 |
| `dexdump` | DEX 文件查看器 |
| `split-select` | APK 分割选择器 |

## 快速开始

### 使用预编译版本

从 [GitHub Releases](../../releases) 下载预编译版本。

### 从源码编译

#### 前置条件

- Docker (Docker Desktop 4.x+ 或 Docker Engine 20.10+)
- 磁盘空间: ~15 GB
- 内存: 8 GB 以上

#### 编译步骤

```bash
# 1. 克隆本仓库
git clone <this-repo>
cd android-build-tools-aarch64

# 2. 修改配置 (可选)
# 编辑 config.env 设置目标版本
# 默认: AOSP_BRANCH=platform-tools-33.0.1

# 3. 完整编译
make linux-arm64

# 4. 验证结果
make verify

# 5. 创建发布包
make archive
```

#### 分步执行

```bash
# 只构建 Docker 镜像
make image-linux-arm64

# 只获取源码
make fetch

# 只编译 (需要先获取源码)
make build

# 进入编译容器调试
make shell-linux-arm64
```

## 配置

编辑 `config.env` 文件:

```bash
# AOSP 源码标签
# build-tools 33.0.1: platform-tools-33.0.1
# build-tools 33.0.0: android-13.0.0_r1
# build-tools 34.0.0: android-14.0.0_r1
AOSP_BRANCH=platform-tools-33.0.1

# 输出版本标签
BUILD_TOOLS_LABEL=33.0.1

# 并行编译任务数
JOBS=4
```

## 安装

编译完成后，将生成的二进制文件复制到 Android SDK 目录:

```bash
# 假设 ANDROID_HOME 是你的 SDK 路径
ANDROID_HOME=~/Android/Sdk

# 创建目录
mkdir -p $ANDROID_HOME/build-tools/33.0.1

# 复制文件
cp out/linux-arm64/* $ANDROID_HOME/build-tools/33.0.1/

# 验证
$ANDROID_HOME/build-tools/33.0.1/aapt2 version
```

## GitHub Actions

本项目包含 GitHub Actions workflow，可以自动编译:

1. **手动触发**: 在 Actions 页面选择 "Build Android build-tools"，点击 "Run workflow"
2. **标签触发**: 推送 `v*` 格式的标签会自动编译并发布

### 自定义版本

在 workflow_dispatch 中可以指定:
- `aosp_branch`: AOSP 源码标签 (如 `platform-tools-33.0.1`)
- `build_tools_label`: 输出版本标签 (如 `33.0.1`)

## 源代码

所有源代码来自 AOSP 官方仓库，详见 `repos.json`。

主要仓库:
- `platform/frameworks/base` - aapt, aapt2
- `platform/system/tools/aidl` - aidl
- `platform/build` - zipalign
- `platform/dalvik` - dexdump

## 故障排除

### 编译失败: 内存不足

减少并行任务数:
```bash
make linux-arm64 JOBS=2
```

### 编译失败: 磁盘空间不足

清理缓存:
```bash
make distclean
```

### 二进制文件无法运行

检查架构:
```bash
file out/linux-arm64/aapt2
# 应该显示: ELF 64-bit LSB executable, ARM aarch64
```

## 参考项目

- [Commit451/android-arm-build-tools](https://github.com/Commit451/android-arm-build-tools)
- [hamza72x/android-sdk-linux-arm64](https://github.com/hamza72x/android-sdk-linux-arm64)
- [lzhiyong/android-sdk-tools](https://github.com/lzhiyong/android-sdk-tools)

## 许可证

MIT License
