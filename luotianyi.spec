#!/usr/bin/env python3
"""
PyInstaller spec file for Luotianyi Desktop Pet
"""
import sys
import os

block_cipher = None

a = Analysis(
    ['run_image.py'],
    pathex=['src'],
    binaries=[],
    datas=[
        ('images', 'images'),
        ('src', 'src'),
    ],
    hiddenimports=[
        'pygame',
        'PIL',
        'win32api',
        'win32con',
        'win32gui',
        'numpy',
        'tkinter',
        'requests',
    ],
    hookspath=['hooks'],  # 使用自定义钩子目录
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='LuotianyiPet',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='LuotianyiPet',
)
