import pygame
import os


class ImageCharacter:
    def __init__(self, image_dir="images", size=200):
        self.size = size
        self.image_dir = image_dir
        self.images = {}
        self.load_images()

    def load_images(self):
        if not os.path.exists(self.image_dir):
            print(f"警告: 图片目录 '{self.image_dir}' 不存在")
            print("请创建以下图片文件:")
            print(f"  {self.image_dir}/idle.png")
            print(f"  {self.image_dir}/walk.png")
            print(f"  {self.image_dir}/sit.png")
            print(f"  {self.image_dir}/sleep.png")
            print(f"  {self.image_dir}/happy.png")
            print(f"  {self.image_dir}/surprise.png")
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
                    self.images[state] = pygame.transform.scale(
                        image, (self.size, self.size)
                    )
                    print(f"加载图片: {filename}")
                except Exception as e:
                    print(f"加载图片失败 {filename}: {e}")
            else:
                print(f"警告: 缺少图片文件 {filename}")

    def get_sprite(self, state):
        if state in self.images:
            return self.images[state]

        print(f"警告: 状态 '{state}' 的图片未找到，使用默认图片")
        return self.get_default_sprite()

    def get_default_sprite(self):
        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(
            surf, (255, 200, 200), (self.size // 2, self.size // 2), self.size // 3
        )
        pygame.draw.circle(
            surf, (0, 0, 0), (self.size // 2 - 20, self.size // 2 - 10), 8
        )
        pygame.draw.circle(
            surf, (0, 0, 0), (self.size // 2 + 20, self.size // 2 - 10), 8
        )
        pygame.draw.arc(
            surf,
            (255, 100, 100),
            (self.size // 2 - 15, self.size // 2 + 10, 30, 20),
            0,
            3.14,
            3,
        )
        return surf


class AnimatedCharacter(ImageCharacter):
    def __init__(self, image_dir="images", size=200, frame_delay=100):
        super().__init__(image_dir, size)
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
                            frames.append(
                                pygame.transform.scale(image, (self.size, self.size))
                            )
                        except Exception as e:
                            print(f"加载动画帧失败 {filename}: {e}")

                if frames:
                    self.animations[state] = frames
                    print(f"加载动画: {dirname} ({len(frames)} 帧)")

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
