#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
洛天依桌面助手 - 图片版
打包专用入口点，兼容开发环境和打包后运行
"""
import sys
import os


def get_base_path():
    """获取资源文件的基础路径，兼容开发环境和PyInstaller打包后"""
    if getattr(sys, "frozen", False):
        # PyInstaller 打包后，数据文件在 sys._MEIPASS 目录（即 _internal/）
        return sys._MEIPASS
    else:
        # 开发环境
        return os.path.dirname(os.path.abspath(__file__))


def check_dependencies():
    """检查依赖是否安装"""
    try:
        import pygame
        import PIL
        import win32api
        import numpy
        return True
    except ImportError as e:
        print(f"缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return False


def show_welcome():
    """显示欢迎信息和功能说明"""
    print("=" * 50)
    print("洛天依桌面助手 v1.0 (图片版)")
    print("=" * 50)

    if not getattr(sys, "frozen", False):
        # 开发环境：检查依赖
        if not check_dependencies():
            print("\n按任意键退出...")
            input()
            sys.exit(1)

    # 显示图片目录结构（仅开发环境）
    if not getattr(sys, "frozen", False) and os.path.exists("images"):
        print("\n图片目录结构:")
        for root, dirs, files in os.walk("images"):
            level = root.replace("images", "").count(os.sep)
            indent = "  " * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = "  " * (level + 1)
            image_files = [f for f in files if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]
            for file in image_files[:5]:
                print(f"{subindent}{file}")
            if len(image_files) > 5:
                print(f"{subindent}... 还有 {len(image_files) - 5} 个图片文件")
    elif not getattr(sys, "frozen", False) and not os.path.exists("images"):
        print("\n警告: images/ 目录不存在")
        print("请创建 images/ 目录并放入洛天依图片")
        print("详细说明请查看 images/README.txt")

    print("\n功能说明:")
    print("  左键拖拽: 移动洛天依")
    print("  右键点击: 打开菜单")
    print("  鼠标悬停: 触发互动")
    print("  ESC键: 退出程序")


def main():
    """主函数"""
    base_path = get_base_path()
    os.chdir(base_path)
    sys.path.insert(0, os.path.join(base_path, "src"))

    # 打包环境不显示控制台，所以只在开发环境显示欢迎信息
    if not getattr(sys, "frozen", False):
        show_welcome()
        print("\n正在启动洛天依桌面助手(图片版)...")

    try:
        from desktop_pet_image import DesktopPetImage

        # 选择动画模式
        use_animation = False
        if not getattr(sys, "frozen", False):
            # 开发环境：询问用户
            try:
                response = input("\n是否使用动画模式? (y/n, 默认n): ").lower()
                use_animation = response == "y"
            except (EOFError, KeyboardInterrupt):
                # 处理可能的输入中断
                use_animation = False
        # 打包环境：默认不使用动画模式

        if not getattr(sys, "frozen", False):
            print(f"\n使用{'动画' if use_animation else '图片'}模式")
            print("启动成功！洛天依已出现在桌面右下角")
            print("正在运行... (按ESC退出)")

        pet = DesktopPetImage(use_animation=use_animation)
        pet.run()

    except Exception as e:
        import traceback

        traceback.print_exc()
        # 在打包环境中避免使用input()，防止"lost sys.stdin"错误
        if not getattr(sys, "frozen", False):
            input("按任意键退出...")
        else:
            # 打包环境：等待一段时间让用户看到错误信息
            import time
            time.sleep(5)


if __name__ == "__main__":
    main()
