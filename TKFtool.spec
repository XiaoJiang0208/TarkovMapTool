# -*- mode: python ; coding: utf-8 -*-

# 打包
a = Analysis(
    ['TKFtool.py'],  # 指定需要打包的Python脚本文件名
    pathex=[],  # 指定额外的搜索路径，默认为空
    binaries=[],  # 指定额外的二进制文件和共享库，默认为空
    datas=[],  # 指定额外的数据文件，默认为空
    hiddenimports=[],  # 指定隐藏的导入（有些库可能不会被自动检测到），默认为空
    hookspath=[],  # 指定自定义hook文件的路径，默认为空
    hooksconfig={},  # 配置hook，默认为空
    runtime_hooks=[],  # 指定运行时hook脚本，默认为空
    excludes=[],  # 指定要排除的模块，默认为空
    noarchive=False,  # 如果为True，不会将Python文件编译为归档，而是直接复制，通常用于调试
)

# 创建一个PYZ对象，它是一个Python归档文件，包含了所有的Python脚本文件
pyz = PYZ(a.pure)

# 创建一个EXE对象，它是最终的可执行文件
exe = EXE(
    pyz,  # 上面创建的PYZ对象
    a.scripts,  # 从Analysis对象中获取的脚本列表
    a.binaries,  # 从Analysis对象中获取的二进制文件列表
    a.datas,  # 从Analysis对象中获取的数据文件列表
    [],  # 额外的依赖文件，默认为空
    name='TKFtool',  # 生成的EXE文件名
    debug=False,  # 是否开启调试模式，开启后可以打印日志等信息
    bootloader_ignore_signals=False,  # Bootloader是否忽略信号
    strip=False,  # 是否移除符号表，减小可执行文件体积（主要用于Linux）
    upx=True,  # 是否使用UPX压缩可执行文件和动态库
    upx_exclude=[],  # 指定不被UPX压缩的文件列表
    runtime_tmpdir=None,  # 指定运行时临时目录
    console=True,  # 是否有控制台窗口，对于命令行工具应为True
    disable_windowed_traceback=False,  # 在窗口化模式下是否禁用traceback
    argv_emulation=False,  # 是否模拟命令行参数传递
    target_arch=None,  # 目标架构
    codesign_identity=None,  # 代码签名身份（主要用于macOS）
    entitlements_file=None,  # 权限文件路径（主要用于macOS）
)
