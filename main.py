#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
洛天依桌面助手
一个可爱的桌面宠物应用
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
    print("洛天依桌面助手 v1.0")
    print("=" * 50)

    if not check_dependencies():
        print("\n按任意键退出...")
        input()
        sys.exit(1)

    print("\n正在启动洛天依桌面助手...")
    print("功能说明:")
    print("  左键拖拽: 移动洛天依")
    print("  右键点击: 打开菜单")
    print("  鼠标悬停: 触发互动")
    print("  ESC键: 退出程序")
    print("\n洛天依会:")
    print("  自动走动、坐下、睡觉")
    print("  随机说话和卖萌")
    print("  根据时间问候")

    try:
        from src.desktop_pet import DesktopPet

        pet = DesktopPet()
        print("\n启动成功！洛天依已出现在桌面右下角")
        print("正在运行... (按ESC退出)")
        pet.run()
    except Exception as e:
        print(f"\n启动失败: {e}")
        print("请确保:")
        print("  1. 已安装所有依赖")
        print("  2. 系统支持透明窗口")
        print("  3. 没有其他程序占用显示")
        print("\n按任意键退出...")
        input()
        sys.exit(1)


if __name__ == "__main__":
    main()
