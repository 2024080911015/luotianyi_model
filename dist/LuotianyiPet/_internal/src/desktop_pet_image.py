import pygame
import sys
import random
import time
import math
import win32api
import win32con
import win32gui
from image_character import ImageCharacter, AnimatedCharacter


class DesktopPetImage:
    def __init__(self, use_animation=False):
        pygame.init()

        self.screen_width = win32api.GetSystemMetrics(0)
        self.screen_height = win32api.GetSystemMetrics(1)

        self.pet_width = 200
        self.pet_height = 280  # 角色高度比宽度大，更符合人物比例
        self.use_animation = use_animation

        # 窗口大小：角色大小 + 上方留给气泡的空间
        self.bubble_area_height = 60
        self.window_width = self.pet_width
        self.window_height = self.pet_height + self.bubble_area_height

        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height), pygame.NOFRAME | pygame.SRCALPHA
        )
        pygame.display.set_caption("Luotianyi Desktop Pet")

        # 必须在 display.set_mode() 之后创建 character，否则 pygame.image.load() 会失败
        if use_animation:
            self.character = AnimatedCharacter(
                "images", self.pet_width, self.pet_height, frame_delay=100
            )
        else:
            self.character = ImageCharacter("images", self.pet_width, self.pet_height)

        self.hwnd = pygame.display.get_wm_info()["window"]

        # 关键修复：只设置 WS_EX_LAYERED，不设置 WS_EX_TRANSPARENT
        # WS_EX_TRANSPARENT 会让鼠标事件穿透窗口，导致无法拖拽
        win32gui.SetWindowLong(
            self.hwnd,
            win32con.GWL_EXSTYLE,
            win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE)
            | win32con.WS_EX_LAYERED,
        )

        # 使用 colorkey 让黑色背景透明
        self.colorkey = (1, 1, 1)  # 用近黑色作为透明色，避免角色本身的黑色被透掉
        win32gui.SetLayeredWindowAttributes(
            self.hwnd,
            win32api.RGB(*self.colorkey),
            0,
            win32con.LWA_COLORKEY,
        )

        # 初始位置：屏幕右下角
        self.x = self.screen_width - self.window_width - 80
        self.y = self.screen_height - self.window_height - 80

        win32gui.SetWindowPos(
            self.hwnd,
            win32con.HWND_TOPMOST,
            int(self.x),
            int(self.y),
            self.window_width,
            self.window_height,
            0,
        )

        # 拖拽相关
        self.dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0

        # 状态
        self.state = "idle"
        self.state_timer = pygame.time.get_ticks()
        self.state_duration = random.randint(3000, 8000)

        # 动画
        self.animation_frame = 0.0
        self.animation_speed = 0.1

        # 气泡对话
        self.bubble_text = ""
        self.bubble_timer = 0
        self.bubble_duration = 3000

        # 鼠标交互
        self.mouse_over = False
        self.click_timer = 0
        self.warned_once = {}  # 防止重复打印警告

        self.dialogs = [
            "你好呀！我是洛天依~",
            "今天天气真好呢！",
            "要听我唱歌吗？",
            "工作辛苦啦，休息一下吧！",
            "喵~（卖萌）",
            "想和我一起玩吗？",
            "注意休息哦，别太累啦！",
            "今天的你也很棒呢！",
            "要加油哦！",
            "我在这里陪着你呢~",
        ]

        self.clock = pygame.time.Clock()
        self.running = True

    def update_position(self):
        win32gui.SetWindowPos(
            self.hwnd,
            win32con.HWND_TOPMOST,
            int(self.x),
            int(self.y),
            self.window_width,
            self.window_height,
            0,
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                if event.button == 1:
                    # 点击区域：角色所在区域
                    pet_rect = pygame.Rect(
                        0, self.bubble_area_height, self.pet_width, self.pet_height
                    )
                    if pet_rect.collidepoint(mouse_x, mouse_y):
                        self.dragging = True
                        # 记录鼠标在屏幕上的绝对位置
                        self.drag_start_x, self.drag_start_y = win32api.GetCursorPos()
                        self.state = "surprise"
                        self.state_timer = pygame.time.get_ticks()
                        self.show_bubble("哎呀！别抓我~")

                elif event.button == 3:
                    self.show_context_menu()

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.dragging:
                    self.dragging = False
                    self.state = "happy"
                    self.state_timer = pygame.time.get_ticks()
                    self.state_duration = 2000

            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    # 用屏幕绝对坐标计算偏移，避免窗口坐标跳动
                    cur_x, cur_y = win32api.GetCursorPos()
                    dx = cur_x - self.drag_start_x
                    dy = cur_y - self.drag_start_y

                    self.x += dx
                    self.y += dy

                    # 限制在屏幕范围内
                    self.x = max(0, min(self.x, self.screen_width - self.window_width))
                    self.y = max(
                        0, min(self.y, self.screen_height - self.window_height)
                    )

                    self.update_position()

                    self.drag_start_x = cur_x
                    self.drag_start_y = cur_y

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update_state(self):
        current_time = pygame.time.get_ticks()

        if self.dragging:
            return

        if current_time - self.state_timer > self.state_duration:
            self.state_timer = current_time

            if self.state == "idle":
                next_states = ["walk", "sit", "happy", "sleep"]
                weights = [0.4, 0.3, 0.2, 0.1]
                self.state = random.choices(next_states, weights=weights)[0]

                if self.state == "walk":
                    self.state_duration = random.randint(2000, 5000)
                    self.show_bubble(
                        random.choice(["走一走~", "活动一下！", "散步时间！"])
                    )
                elif self.state == "sit":
                    self.state_duration = random.randint(4000, 8000)
                    self.show_bubble("坐一会儿~")
                elif self.state == "happy":
                    self.state_duration = random.randint(2000, 4000)
                    self.show_bubble(random.choice(self.dialogs))
                elif self.state == "sleep":
                    self.state_duration = random.randint(10000, 20000)
                    self.show_bubble("Zzz... 好困...")

            elif self.state in ["walk", "sit", "happy", "sleep", "surprise"]:
                self.state = "idle"
                self.state_duration = random.randint(3000, 8000)

        # 气泡消失
        if self.bubble_text and current_time - self.bubble_timer > self.bubble_duration:
            self.bubble_text = ""

        self.animation_frame += self.animation_speed

    def show_bubble(self, text):
        self.bubble_text = text
        self.bubble_timer = pygame.time.get_ticks()

    def show_context_menu(self):
        import tkinter as tk
        from tkinter import messagebox

        def exit_app():
            self.running = False
            root.destroy()

        def set_size(new_width):
            # 固定比例 1.4 (280/200)
            ratio = 1.4
            self.pet_width = new_width
            self.pet_height = int(new_width * ratio)
            self.window_width = self.pet_width
            self.window_height = self.pet_height + self.bubble_area_height
            
            # 先设置新的窗口大小
            self.screen = pygame.display.set_mode(
                (self.window_width, self.window_height),
                pygame.NOFRAME | pygame.SRCALPHA,
            )
            
            # 重新获取窗口句柄并设置属性
            self.hwnd = pygame.display.get_wm_info()["window"]
            win32gui.SetWindowLong(
                self.hwnd,
                win32con.GWL_EXSTYLE,
                win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE)
                | win32con.WS_EX_LAYERED,
            )
            win32gui.SetLayeredWindowAttributes(
                self.hwnd,
                win32api.RGB(*self.colorkey),
                0,
                win32con.LWA_COLORKEY,
            )
            win32gui.SetWindowPos(
                self.hwnd,
                win32con.HWND_TOPMOST,
                int(self.x),
                int(self.y),
                self.window_width,
                self.window_height,
                0,
            )
            
            # 然后重新加载角色图片（使用新尺寸）
            if self.use_animation:
                self.character = AnimatedCharacter(
                    "images", self.pet_width, self.pet_height, frame_delay=100
                )
            else:
                self.character = ImageCharacter(
                    "images", self.pet_width, self.pet_height
                )

        def toggle_animation():
            self.use_animation = not self.use_animation
            if self.use_animation:
                self.character = AnimatedCharacter(
                    "images", self.pet_width, self.pet_height, frame_delay=100
                )
            else:
                self.character = ImageCharacter(
                    "images", self.pet_width, self.pet_height
                )

        def show_about():
            messagebox.showinfo("About", "Luotianyi Desktop Pet v1.0")

        root = tk.Tk()
        root.withdraw()

        menu = tk.Menu(root, tearoff=0)
        menu.add_command(
            label="Say", command=lambda: self.show_bubble(random.choice(self.dialogs))
        )
        
        # 使用子菜单选择大小
        size_menu = tk.Menu(menu, tearoff=0)
        size_menu.add_command(label="Small (120)", command=lambda: set_size(120))
        size_menu.add_command(label="Medium (200)", command=lambda: set_size(200))
        size_menu.add_command(label="Large (280)", command=lambda: set_size(280))
        menu.add_cascade(label="Resize", menu=size_menu)
        
        menu.add_command(
            label=f"{'Disable' if self.use_animation else 'Enable'} Animation",
            command=toggle_animation,
        )
        menu.add_separator()
        menu.add_command(label="About", command=show_about)
        menu.add_separator()
        menu.add_command(label="Exit", command=exit_app)

        try:
            x, y = win32api.GetCursorPos()
            menu.tk_popup(x, y, 0)
        finally:
            root.update()

    def draw(self):
        # 用 colorkey 颜色填充背景（这个颜色会被透明掉）
        self.screen.fill(self.colorkey)

        current_time = pygame.time.get_ticks()

        if self.use_animation:
            sprite = self.character.get_sprite(self.state, current_time)
        else:
            sprite = self.character.get_sprite(self.state)

        # 角色绘制在气泡区域下方
        draw_x = 0
        draw_y = self.bubble_area_height

        if self.state == "walk":
            offset = int(math.sin(self.animation_frame) * 5)
            self.screen.blit(sprite, (draw_x + offset, draw_y))
        else:
            self.screen.blit(sprite, (draw_x, draw_y))

        if self.bubble_text:
            self.draw_bubble(self.bubble_text)

        pygame.display.flip()

    def draw_bubble(self, text):
        try:
            font = pygame.font.SysFont("simhei", 14)
        except Exception:
            font = pygame.font.SysFont(None, 18)

        # 中文逐字换行
        lines = []
        current_line = ""
        max_width = self.window_width - 20

        for char in text:
            test_line = current_line + char
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = char

        if current_line:
            lines.append(current_line)

        line_height = 20
        bubble_height = len(lines) * line_height + 12
        bubble_width = min(max_width + 16, self.window_width)
        bubble_x = (self.window_width - bubble_width) // 2
        bubble_y = max(0, self.bubble_area_height - bubble_height - 5)

        # 气泡背景
        bubble_surf = pygame.Surface((bubble_width, bubble_height), pygame.SRCALPHA)
        pygame.draw.rect(
            bubble_surf,
            (255, 255, 255, 220),
            (0, 0, bubble_width, bubble_height),
            border_radius=8,
        )
        pygame.draw.rect(
            bubble_surf,
            (180, 180, 180, 200),
            (0, 0, bubble_width, bubble_height),
            2,
            border_radius=8,
        )
        self.screen.blit(bubble_surf, (bubble_x, bubble_y))

        # 气泡文字
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(
                center=(
                    self.window_width // 2,
                    bubble_y + 8 + i * line_height + line_height // 2,
                )
            )
            self.screen.blit(text_surface, text_rect)

    def run(self):
        while self.running:
            self.handle_events()
            self.update_state()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    pet = DesktopPetImage(use_animation=False)
    pet.run()
