import pygame
import sys
import random
import time
import math
import threading
import win32api
import win32con
import win32gui
from .character_generator import LuotianyiCharacter
from .info_service import get_weather, get_time_info, get_greeting


class DesktopPet:
    def __init__(self):
        pygame.init()

        self.screen_width = win32api.GetSystemMetrics(0)
        self.screen_height = win32api.GetSystemMetrics(1)

        self.pet_size = 200
        self.character = LuotianyiCharacter(self.pet_size)

        self.window_width = self.pet_size + 100
        self.window_height = self.pet_size + 100

        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height), pygame.NOFRAME | pygame.SRCALPHA
        )
        pygame.display.set_caption("洛天依桌面助手")

        hwnd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowLong(
            hwnd,
            win32con.GWL_EXSTYLE,
            win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            | win32con.WS_EX_LAYERED
            | win32con.WS_EX_TRANSPARENT,
        )

        win32gui.SetLayeredWindowAttributes(
            hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY
        )

        self.x = self.screen_width - self.window_width - 50
        self.y = self.screen_height - self.window_height - 50

        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_TOPMOST,
            int(self.x),
            int(self.y),
            self.window_width,
            self.window_height,
            0,
        )

        self.dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        self.state = "idle"
        self.state_timer = 0
        self.state_duration = random.randint(3000, 8000)

        self.animation_frame = 0
        self.animation_speed = 0.1

        self.bubble_text = ""
        self.bubble_timer = 0
        self.bubble_duration = 3000

        self.mouse_over = False
        self.click_timer = 0

        # 用于线程安全的气泡更新（天气查询等异步操作）
        self._pending_bubble = None
        self._pending_lock = threading.Lock()

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
        hwnd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowPos(
            hwnd,
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
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if event.button == 1:
                    pet_rect = pygame.Rect(50, 50, self.pet_size, self.pet_size)
                    if pet_rect.collidepoint(mouse_x, mouse_y):
                        self.dragging = True
                        self.drag_offset_x = mouse_x
                        self.drag_offset_y = mouse_y
                        self.state = "surprise"
                        self.state_timer = 0
                        self.show_bubble("哎呀！别抓我~")

                elif event.button == 3:
                    self.show_context_menu()

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False
                    if self.state == "surprise":
                        self.state = "happy"
                        self.state_timer = 0
                        self.state_duration = 2000

            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    dx = mouse_x - self.drag_offset_x
                    dy = mouse_y - self.drag_offset_y

                    self.x += dx
                    self.y += dy

                    self.x = max(0, min(self.x, self.screen_width - self.window_width))
                    self.y = max(
                        0, min(self.y, self.screen_height - self.window_height)
                    )

                    self.update_position()

                    self.drag_offset_x = mouse_x
                    self.drag_offset_y = mouse_y

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update_state(self):
        current_time = pygame.time.get_ticks()

        # 处理异步回调的气泡更新（如天气查询结果）
        with self._pending_lock:
            if self._pending_bubble is not None:
                self.show_bubble(self._pending_bubble)
                self.state = "happy"
                self.state_timer = current_time
                self.state_duration = 5000
                self._pending_bubble = None

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

        if self.bubble_text and current_time - self.bubble_timer > self.bubble_duration:
            self.bubble_text = ""

        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen_mouse_x = self.x + mouse_x
        screen_mouse_y = self.y + mouse_y

        pet_screen_rect = pygame.Rect(
            self.x + 50, self.y + 50, self.pet_size, self.pet_size
        )

        if pet_screen_rect.collidepoint(screen_mouse_x, screen_mouse_y):
            if not self.mouse_over:
                self.mouse_over = True
                self.click_timer = current_time
                if self.state != "surprise" and self.state != "happy":
                    self.state = "happy"
                    self.state_timer = current_time
                    self.state_duration = 2000
        else:
            self.mouse_over = False

        if self.mouse_over and current_time - self.click_timer > 5000:
            if random.random() < 0.01:
                self.show_bubble(
                    random.choice(["你在看我吗？", "我可爱吗？", "想和我玩吗？"])
                )
                self.click_timer = current_time

        self.animation_frame += self.animation_speed

    def show_bubble(self, text):
        self.bubble_text = text
        self.bubble_timer = pygame.time.get_ticks()

    def _set_pending_bubble(self, text):
        """线程安全地设置待显示的气泡文本（供异步回调使用）"""
        with self._pending_lock:
            self._pending_bubble = text

    def show_context_menu(self):
        import tkinter as tk
        from tkinter import messagebox

        def exit_app():
            self.running = False
            root.quit()

        def query_weather():
            self.show_bubble("正在查询天气...")
            self.state = "happy"
            self.state_timer = pygame.time.get_ticks()
            self.state_duration = 10000
            get_weather(self._set_pending_bubble)

        def query_time():
            info = get_time_info()
            self.show_bubble(info)
            self.state = "happy"
            self.state_timer = pygame.time.get_ticks()
            self.state_duration = 5000

        def query_greeting():
            greeting = get_greeting()
            self.show_bubble(greeting)
            self.state = "happy"
            self.state_timer = pygame.time.get_ticks()
            self.state_duration = 5000

        def change_size():
            size_window = tk.Toplevel(root)
            size_window.title("调整大小")
            size_window.geometry("200x100")

            tk.Label(size_window, text="选择大小:").pack(pady=10)

            size_var = tk.IntVar(value=self.pet_size)

            def apply_size():
                self.pet_size = size_var.get()
                self.character = LuotianyiCharacter(self.pet_size)
                self.window_width = self.pet_size + 100
                self.window_height = self.pet_size + 100
                self.screen = pygame.display.set_mode(
                    (self.window_width, self.window_height),
                    pygame.NOFRAME | pygame.SRCALPHA,
                )
                size_window.destroy()

            tk.Radiobutton(
                size_window, text="小 (150)", variable=size_var, value=150
            ).pack()
            tk.Radiobutton(
                size_window, text="中 (200)", variable=size_var, value=200
            ).pack()
            tk.Radiobutton(
                size_window, text="大 (250)", variable=size_var, value=250
            ).pack()

            tk.Button(size_window, text="应用", command=apply_size).pack(pady=10)

        def show_about():
            messagebox.showinfo(
                "关于", "洛天依桌面助手 v1.0\n\n一个可爱的桌面宠物应用\n作者: 你的助手"
            )

        root = tk.Tk()
        root.withdraw()

        menu = tk.Menu(root, tearoff=0)
        menu.add_command(
            label="说话", command=lambda: self.show_bubble(random.choice(self.dialogs))
        )

        # 互动查询子菜单
        query_menu = tk.Menu(menu, tearoff=0)
        query_menu.add_command(label="🌤 查询天气", command=query_weather)
        query_menu.add_command(label="🕐 查询时间", command=query_time)
        query_menu.add_command(label="👋 今日问候", command=query_greeting)
        menu.add_cascade(label="互动查询", menu=query_menu)

        menu.add_command(label="调整大小", command=change_size)
        menu.add_separator()
        menu.add_command(label="关于", command=show_about)
        menu.add_separator()
        menu.add_command(label="退出", command=exit_app)

        try:
            menu.tk_popup(win32api.GetCursorPos()[0], win32api.GetCursorPos()[1])
        finally:
            root.update()

    def draw(self):
        self.screen.fill((0, 0, 0, 0))

        sprite = self.character.get_sprite(self.state)

        if self.state == "walk":
            offset = int(math.sin(self.animation_frame) * 5)
            self.screen.blit(sprite, (50 + offset, 50))
        else:
            self.screen.blit(sprite, (50, 50))

        if self.bubble_text:
            self.draw_bubble(self.bubble_text)

        pygame.display.flip()

    def draw_bubble(self, text):
        font = pygame.font.SysFont("simhei", 16)

        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= 180:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "

        if current_line:
            lines.append(current_line)

        bubble_height = len(lines) * 25 + 20
        bubble_width = 200

        bubble_x = 150 - bubble_width // 2
        bubble_y = 20

        pygame.draw.rect(
            self.screen,
            (255, 255, 255, 230),
            (bubble_x, bubble_y, bubble_width, bubble_height),
            border_radius=10,
        )

        pygame.draw.rect(
            self.screen,
            (200, 200, 200, 200),
            (bubble_x, bubble_y, bubble_width, bubble_height),
            2,
            border_radius=10,
        )

        for i, line in enumerate(lines):
            text_surface = font.render(line.strip(), True, (0, 0, 0))
            text_rect = text_surface.get_rect(
                center=(bubble_x + bubble_width // 2, bubble_y + 15 + i * 25)
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
    pet = DesktopPet()
    pet.run()
