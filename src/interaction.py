import pygame
import random
import time
import json
import os


class InteractionManager:
    def __init__(self, pet):
        self.pet = pet
        self.interactions = []
        self.last_interaction_time = time.time()
        self.interaction_cooldown = 5

        self.load_interactions()

    def load_interactions(self):
        interaction_file = "interactions.json"
        if os.path.exists(interaction_file):
            with open(interaction_file, "r", encoding="utf-8") as f:
                self.interactions = json.load(f)
        else:
            self.interactions = [
                {
                    "type": "click",
                    "response": "happy",
                    "dialog": "哎呀，好痒~",
                    "duration": 2000,
                },
                {
                    "type": "click",
                    "response": "surprise",
                    "dialog": "哇！吓我一跳！",
                    "duration": 1500,
                },
                {
                    "type": "hover",
                    "response": "happy",
                    "dialog": "你在看我吗？",
                    "duration": 3000,
                },
                {
                    "type": "idle",
                    "response": "sit",
                    "dialog": "有点无聊呢...",
                    "duration": 5000,
                },
                {
                    "type": "time_morning",
                    "response": "happy",
                    "dialog": "早上好！新的一天开始啦！",
                    "duration": 4000,
                },
                {
                    "type": "time_night",
                    "response": "sleep",
                    "dialog": "晚安，做个好梦~",
                    "duration": 6000,
                },
            ]

    def handle_click(self, x, y):
        current_time = time.time()
        if current_time - self.last_interaction_time < self.interaction_cooldown:
            return

        pet_rect = pygame.Rect(50, 50, self.pet.pet_size, self.pet.pet_size)
        if pet_rect.collidepoint(x, y):
            self.last_interaction_time = current_time

            click_interactions = [i for i in self.interactions if i["type"] == "click"]
            if click_interactions:
                interaction = random.choice(click_interactions)
                self.apply_interaction(interaction)
                return True

        return False

    def handle_hover(self, x, y):
        current_time = time.time()
        if current_time - self.last_interaction_time < self.interaction_cooldown:
            return

        pet_rect = pygame.Rect(50, 50, self.pet.pet_size, self.pet.pet_size)
        if pet_rect.collidepoint(x, y):
            self.last_interaction_time = current_time

            if random.random() < 0.1:
                hover_interactions = [
                    i for i in self.interactions if i["type"] == "hover"
                ]
                if hover_interactions:
                    interaction = random.choice(hover_interactions)
                    self.apply_interaction(interaction)
                    return True

        return False

    def handle_time_based(self):
        current_hour = time.localtime().tm_hour

        if 6 <= current_hour < 12:
            time_type = "time_morning"
        elif 18 <= current_hour < 24:
            time_type = "time_night"
        else:
            return

        time_interactions = [i for i in self.interactions if i["type"] == time_type]
        if time_interactions and random.random() < 0.05:
            interaction = random.choice(time_interactions)
            self.apply_interaction(interaction)
            return True

        return False

    def handle_idle(self):
        current_time = time.time()
        if current_time - self.last_interaction_time > 30:
            if random.random() < 0.02:
                idle_interactions = [
                    i for i in self.interactions if i["type"] == "idle"
                ]
                if idle_interactions:
                    interaction = random.choice(idle_interactions)
                    self.apply_interaction(interaction)
                    return True

        return False

    def apply_interaction(self, interaction):
        self.pet.state = interaction["response"]
        self.pet.state_timer = pygame.time.get_ticks()
        self.pet.state_duration = interaction.get("duration", 3000)

        if "dialog" in interaction:
            self.pet.show_bubble(interaction["dialog"])

    def update(self):
        self.handle_time_based()
        self.handle_idle()

    def add_interaction(self, interaction_type, response, dialog, duration=3000):
        new_interaction = {
            "type": interaction_type,
            "response": response,
            "dialog": dialog,
            "duration": duration,
        }
        self.interactions.append(new_interaction)

        self.save_interactions()

    def save_interactions(self):
        with open("interactions.json", "w", encoding="utf-8") as f:
            json.dump(self.interactions, f, ensure_ascii=False, indent=2)


class DialogSystem:
    def __init__(self):
        self.dialogs = {
            "greeting": ["你好！我是洛天依~", "欢迎回来！", "今天过得怎么样？"],
            "encouragement": [
                "加油！你可以的！",
                "别放弃，坚持就是胜利！",
                "相信自己，你是最棒的！",
            ],
            "weather": [
                "今天天气真好呢！",
                "下雨了，记得带伞哦~",
                "有点冷，多穿点衣服！",
            ],
            "time": ["该休息一下啦！", "工作辛苦了！", "记得按时吃饭哦~"],
            "random": [
                "喵~（卖萌）",
                "要听我唱歌吗？",
                "我在这里陪着你呢~",
                "今天的你也很可爱呢！",
            ],
        }

        self.dialog_history = []
        self.max_history = 10

    def get_dialog(self, category=None):
        if category and category in self.dialogs:
            dialog = random.choice(self.dialogs[category])
        else:
            all_dialogs = []
            for cat in self.dialogs.values():
                all_dialogs.extend(cat)
            dialog = random.choice(all_dialogs)

        self.dialog_history.append(
            {"time": time.time(), "dialog": dialog, "category": category}
        )

        if len(self.dialog_history) > self.max_history:
            self.dialog_history.pop(0)

        return dialog

    def add_dialog(self, category, dialog):
        if category not in self.dialogs:
            self.dialogs[category] = []

        self.dialogs[category].append(dialog)

    def get_context_dialog(self, context):
        current_hour = time.localtime().tm_hour

        if context == "morning" and 6 <= current_hour < 12:
            return self.get_dialog("greeting")
        elif context == "work" and 9 <= current_hour < 18:
            return self.get_dialog("encouragement")
        elif context == "evening" and 18 <= current_hour < 24:
            return self.get_dialog("time")
        else:
            return self.get_dialog("random")


class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.muted = False

        try:
            pygame.mixer.init()
            self.load_sounds()
        except:
            print("声音初始化失败，将静音运行")
            self.muted = True

    def load_sounds(self):
        sound_files = {
            "click": "click.wav",
            "hover": "hover.wav",
            "dialog": "dialog.wav",
        }

        for name, filename in sound_files.items():
            filepath = os.path.join("sounds", filename)
            if os.path.exists(filepath):
                try:
                    self.sounds[name] = pygame.mixer.Sound(filepath)
                except:
                    print(f"无法加载声音文件: {filename}")

    def play_sound(self, name, volume=0.5):
        if self.muted or name not in self.sounds:
            return

        sound = self.sounds[name]
        sound.set_volume(volume)
        sound.play()

    def toggle_mute(self):
        self.muted = not self.muted
        return self.muted
