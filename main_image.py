#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
洛天依桌面助手 - 图片版
使用外部图片文件
"""

import sys
import os


def check_dependencies():
    try:
        import pygame
        import PIL
        import win32api
        import numpy

        print("所有依赖已安装")
        return True
    except ImportError as e:
        print(f"缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return False


def main():
    print("=" * 50)
    print("洛天依桌面助手 v1.0 (图片版)")
    print("=" * 50)

    if not check_dependencies():
        print("\n按任意键退出...")
        input()
        sys.exit(1)

    print("\n图片目录结构:")
    if os.path.exists("images"):
        print("images/ 目录存在")
        for root, dirs, files in os.walk("images"):
            level = root.replace("images", "").count(os.sep)
            indent = "  " * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = "  " * (level + 1)
            for file in files[:5]:
                if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                    print(f"{subindent}{file}")
            if len(files) > 5:
                print(f"{subindent}... 还有 {len(files) - 5} 个文件")
    else:
        print("images/ 目录不存在")
        print("请创建 images/ 目录并放入洛天依图片")
        print("详细说明请查看 images/README.txt")

    print("\n正在启动洛天依桌面助手(图片版)...")
    print("功能说明:")
    print("  左键拖拽: 移动洛天依")
    print("  右键点击: 打开菜单")
    print("  鼠标悬停: 触发互动")
    print("  ESC键: 退出程序")

    try:
        import sys

        sys.path.insert(0, "src")
        from desktop_pet_image import DesktopPetImage

        use_animation = input("\n是否使用动画模式? (y/n, 默认n): ").lower() == "y"
        pet = DesktopPetImage(use_animation=use_animation)
        print("\n启动成功！洛天依已出现在桌面右下角")
        print("正在运行... (按ESC退出)")
        pet.run()
    except Exception as e:
        print(f"\n启动失败: {e}")
        print("请确保:")
        print("  1. 已安装所有依赖")
        print("  2. 系统支持透明窗口")
        print("  3. 图片格式正确")
        print("\n按任意键退出...")
        input()
        sys.exit(1)


if __name__ == "__main__":
    main()
