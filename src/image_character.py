import pygame
import os


class ImageCharacter:
    def __init__(self, image_dir="images", width=200, height=280):
        self.width = width
        self.height = height
        self.image_dir = image_dir
        self.images = {}
        self._default_sprite = None
        self.load_images()

    def load_images(self):
        if not os.path.exists(self.image_dir):
            print(f"Image directory '{self.image_dir}' not found")
            return

        image_files = {
            "idle": "idle.png",
            "walk": "walk.png",
            "sit": "sit.png",
            "sleep": "sleep.png",
            "happy": "happy.png",
            "surprise": "surprise.png",
        }

        for state, filename in image_files.items():
            filepath = os.path.join(self.image_dir, filename)
            if os.path.exists(filepath):
                try:
                    image = pygame.image.load(filepath)
                    # 保持原图比例缩放到目标区域内
                    image = self._scale_keep_ratio(image)
                    self.images[state] = image
                    print(f"Loaded: {filename}")
                except Exception as e:
                    print(f"Failed to load {filename}: {e}")
            else:
                print(f"Missing: {filename}")

    def _scale_keep_ratio(self, image):
        """缩放图片，保持宽高比，适应目标区域"""
        orig_w, orig_h = image.get_size()
        ratio = min(self.width / orig_w, self.height / orig_h)
        new_w = int(orig_w * ratio)
        new_h = int(orig_h * ratio)
        scaled = pygame.transform.smoothscale(image, (new_w, new_h))

        # 创建目标大小的透明surface，居中放置
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        x = (self.width - new_w) // 2
        y = self.height - new_h  # 底部对齐
        surf.blit(scaled, (x, y))
        return surf

    def get_sprite(self, state):
        if state in self.images:
            return self.images[state]

        # 只在第一次警告
        return self.get_default_sprite()

    def get_default_sprite(self):
        if self._default_sprite is not None:
            return self._default_sprite

        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        cx = self.width // 2
        # 头
        head_r = 35
        head_y = 60
        pygame.draw.circle(surf, (255, 228, 220), (cx, head_y), head_r)

        # 头发（灰蓝色，洛天依特征）
        hair_color = (100, 120, 160)
        pygame.draw.ellipse(surf, hair_color, (cx - 38, head_y - 42, 76, 50))
        # 左右双马尾
        pygame.draw.ellipse(surf, hair_color, (cx - 55, head_y - 20, 25, 60))
        pygame.draw.ellipse(surf, hair_color, (cx + 30, head_y - 20, 25, 60))

        # 眼睛
        pygame.draw.ellipse(surf, (60, 80, 140), (cx - 16, head_y - 8, 10, 12))
        pygame.draw.ellipse(surf, (60, 80, 140), (cx + 6, head_y - 8, 10, 12))
        # 高光
        pygame.draw.circle(surf, (255, 255, 255), (cx - 13, head_y - 5), 3)
        pygame.draw.circle(surf, (255, 255, 255), (cx + 9, head_y - 5), 3)

        # 嘴巴
        pygame.draw.arc(surf, (220, 120, 120), (cx - 8, head_y + 8, 16, 10), 3.14, 0, 2)

        # 腮红
        pygame.draw.circle(surf, (255, 200, 200, 120), (cx - 22, head_y + 5), 7)
        pygame.draw.circle(surf, (255, 200, 200, 120), (cx + 22, head_y + 5), 7)

        # 身体
        body_top = head_y + head_r - 5
        body_color = (180, 200, 230)
        pygame.draw.rect(surf, body_color, (cx - 22, body_top, 44, 55), border_radius=8)

        # 裙子
        skirt_color = (140, 160, 200)
        skirt_top = body_top + 45
        points = [
            (cx - 22, skirt_top),
            (cx - 35, skirt_top + 50),
            (cx + 35, skirt_top + 50),
            (cx + 22, skirt_top),
        ]
        pygame.draw.polygon(surf, skirt_color, points)

        # 腿
        leg_color = (255, 220, 210)
        leg_top = skirt_top + 45
        pygame.draw.rect(surf, leg_color, (cx - 18, leg_top, 10, 55), border_radius=4)
        pygame.draw.rect(surf, leg_color, (cx + 8, leg_top, 10, 55), border_radius=4)

        # 鞋子
        shoe_color = (80, 80, 80)
        shoe_top = leg_top + 50
        pygame.draw.ellipse(surf, shoe_color, (cx - 22, shoe_top, 16, 10))
        pygame.draw.ellipse(surf, shoe_color, (cx + 6, shoe_top, 16, 10))

        # 手臂
        arm_color = (255, 228, 220)
        pygame.draw.rect(
            surf, arm_color, (cx - 32, body_top + 10, 12, 40), border_radius=5
        )
        pygame.draw.rect(
            surf, arm_color, (cx + 20, body_top + 10, 12, 40), border_radius=5
        )

        self._default_sprite = surf
        return surf


class AnimatedCharacter(ImageCharacter):
    def __init__(self, image_dir="images", width=200, height=280, frame_delay=100):
        super().__init__(image_dir, width, height)
        self.frame_delay = frame_delay
        self.current_frame = 0
        self.last_update = 0
        self.animations = {}
        self.load_animations()

    def load_animations(self):
        animation_dirs = {
            "idle": "idle",
            "walk": "walk",
            "sit": "sit",
            "sleep": "sleep",
            "happy": "happy",
            "surprise": "surprise",
        }

        for state, dirname in animation_dirs.items():
            anim_dir = os.path.join(self.image_dir, dirname)
            if os.path.exists(anim_dir) and os.path.isdir(anim_dir):
                frames = []
                for filename in sorted(os.listdir(anim_dir)):
                    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                        filepath = os.path.join(anim_dir, filename)
                        try:
                            image = pygame.image.load(filepath)
                            image = self._scale_keep_ratio(image)
                            frames.append(image)
                        except Exception as e:
                            print(f"Failed to load animation frame {filename}: {e}")

                if frames:
                    self.animations[state] = frames
                    print(f"Loaded animation: {dirname} ({len(frames)} frames)")

    def get_sprite(self, state, current_time=None):
        if state in self.animations:
            if current_time is not None:
                if current_time - self.last_update > self.frame_delay:
                    self.current_frame = (self.current_frame + 1) % len(
                        self.animations[state]
                    )
                    self.last_update = current_time
            return self.animations[state][self.current_frame]

        return super().get_sprite(state)

    def reset_animation(self):
        self.current_frame = 0
        self.last_update = 0
