import pygame
import math
import random
from PIL import Image, ImageDraw


class LuotianyiCharacter:
    def __init__(self, size=200):
        self.size = size
        self.images = {}
        self.generate_sprites()

    def generate_sprites(self):
        self.images["idle"] = self.draw_idle()
        self.images["walk"] = self.draw_walk()
        self.images["sit"] = self.draw_sit()
        self.images["sleep"] = self.draw_sleep()
        self.images["happy"] = self.draw_happy()
        self.images["surprise"] = self.draw_surprise()

    def draw_idle(self):
        img = Image.new("RGBA", (self.size, self.size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        center_x, center_y = self.size // 2, self.size // 2

        self.draw_body(draw, center_x, center_y)
        self.draw_face(draw, center_x, center_y - 20)
        self.draw_hair(draw, center_x, center_y - 20)
        self.draw_clothes(draw, center_x, center_y)

        return pygame.image.fromstring(img.tobytes(), img.size, img.mode)

    def draw_walk(self):
        img = Image.new("RGBA", (self.size, self.size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        center_x, center_y = self.size // 2, self.size // 2

        self.draw_body(draw, center_x, center_y, leg_offset=10)
        self.draw_face(draw, center_x, center_y - 20, eye_offset=5)
        self.draw_hair(draw, center_x, center_y - 20, sway=10)
        self.draw_clothes(draw, center_x, center_y, sway=5)

        return pygame.image.fromstring(img.tobytes(), img.size, img.mode)

    def draw_sit(self):
        img = Image.new("RGBA", (self.size, self.size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        center_x, center_y = self.size // 2, self.size // 2 + 30

        self.draw_body_sitting(draw, center_x, center_y)
        self.draw_face(draw, center_x, center_y - 50)
        self.draw_hair(draw, center_x, center_y - 50)
        self.draw_clothes(draw, center_x, center_y - 20)

        return pygame.image.fromstring(img.tobytes(), img.size, img.mode)

    def draw_sleep(self):
        img = Image.new("RGBA", (self.size, self.size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        center_x, center_y = self.size // 2, self.size // 2

        self.draw_body_sleeping(draw, center_x, center_y)
        self.draw_face_sleeping(draw, center_x, center_y - 20)
        self.draw_hair(draw, center_x, center_y - 20)
        self.draw_clothes(draw, center_x, center_y)

        return pygame.image.fromstring(img.tobytes(), img.size, img.mode)

    def draw_happy(self):
        img = Image.new("RGBA", (self.size, self.size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        center_x, center_y = self.size // 2, self.size // 2

        self.draw_body(draw, center_x, center_y)
        self.draw_face_happy(draw, center_x, center_y - 20)
        self.draw_hair(draw, center_x, center_y - 20)
        self.draw_clothes(draw, center_x, center_y)

        return pygame.image.fromstring(img.tobytes(), img.size, img.mode)

    def draw_surprise(self):
        img = Image.new("RGBA", (self.size, self.size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        center_x, center_y = self.size // 2, self.size // 2

        self.draw_body(draw, center_x, center_y)
        self.draw_face_surprise(draw, center_x, center_y - 20)
        self.draw_hair(draw, center_x, center_y - 20)
        self.draw_clothes(draw, center_x, center_y)

        return pygame.image.fromstring(img.tobytes(), img.size, img.mode)

    def draw_body(self, draw, x, y, leg_offset=0):
        body_color = (255, 230, 240)
        head_radius = 40
        body_width = 60
        body_height = 80
        leg_length = 50

        draw.ellipse(
            [
                x - head_radius,
                y - head_radius - 20,
                x + head_radius,
                y + head_radius - 20,
            ],
            fill=body_color,
        )

        draw.rounded_rectangle(
            [x - body_width // 2, y, x + body_width // 2, y + body_height],
            radius=20,
            fill=body_color,
        )

        draw.line(
            [
                x - 15,
                y + body_height,
                x - 15 - leg_offset,
                y + body_height + leg_length,
            ],
            fill=body_color,
            width=10,
        )
        draw.line(
            [
                x + 15,
                y + body_height,
                x + 15 + leg_offset,
                y + body_height + leg_length,
            ],
            fill=body_color,
            width=10,
        )

        arm_length = 40
        draw.line(
            [x - body_width // 2, y + 20, x - body_width // 2 - arm_length, y + 40],
            fill=body_color,
            width=8,
        )
        draw.line(
            [x + body_width // 2, y + 20, x + body_width // 2 + arm_length, y + 40],
            fill=body_color,
            width=8,
        )

    def draw_body_sitting(self, draw, x, y):
        body_color = (255, 230, 240)
        head_radius = 40
        body_width = 60
        body_height = 60

        draw.ellipse(
            [
                x - head_radius,
                y - head_radius - 50,
                x + head_radius,
                y + head_radius - 50,
            ],
            fill=body_color,
        )

        draw.rounded_rectangle(
            [x - body_width // 2, y - 30, x + body_width // 2, y + body_height - 30],
            radius=15,
            fill=body_color,
        )

        leg_length = 30
        draw.line(
            [x - 20, y + body_height - 30, x - 40, y + body_height + leg_length - 30],
            fill=body_color,
            width=10,
        )
        draw.line(
            [x + 20, y + body_height - 30, x + 40, y + body_height + leg_length - 30],
            fill=body_color,
            width=10,
        )

        arm_length = 30
        draw.line(
            [x - body_width // 2, y, x - body_width // 2 - arm_length, y + 20],
            fill=body_color,
            width=8,
        )
        draw.line(
            [x + body_width // 2, y, x + body_width // 2 + arm_length, y + 20],
            fill=body_color,
            width=8,
        )

    def draw_body_sleeping(self, draw, x, y):
        body_color = (255, 230, 240)
        head_radius = 40
        body_width = 80
        body_height = 60

        draw.ellipse(
            [
                x - head_radius,
                y - head_radius - 20,
                x + head_radius,
                y + head_radius - 20,
            ],
            fill=body_color,
        )

        draw.rounded_rectangle(
            [x - body_width // 2, y, x + body_width // 2, y + body_height],
            radius=20,
            fill=body_color,
        )

        leg_length = 40
        draw.line(
            [x - 25, y + body_height, x - 25, y + body_height + leg_length],
            fill=body_color,
            width=10,
        )
        draw.line(
            [x + 25, y + body_height, x + 25, y + body_height + leg_length],
            fill=body_color,
            width=10,
        )

    def draw_face(self, draw, x, y, eye_offset=0):
        eye_color = (0, 0, 0)
        eye_radius = 8
        mouth_color = (255, 150, 150)

        draw.ellipse(
            [x - 20 - eye_offset, y - 5, x - 10 - eye_offset, y + 5], fill=eye_color
        )
        draw.ellipse(
            [x + 10 + eye_offset, y - 5, x + 20 + eye_offset, y + 5], fill=eye_color
        )

        draw.arc(
            [x - 15, y + 10, x + 15, y + 25],
            start=0,
            end=180,
            fill=mouth_color,
            width=3,
        )

    def draw_face_happy(self, draw, x, y):
        eye_color = (0, 0, 0)
        eye_radius = 8
        mouth_color = (255, 100, 100)

        draw.ellipse([x - 20, y - 5, x - 10, y + 5], fill=eye_color)
        draw.ellipse([x + 10, y - 5, x + 20, y + 5], fill=eye_color)

        draw.arc(
            [x - 15, y + 15, x + 15, y + 30],
            start=0,
            end=180,
            fill=mouth_color,
            width=3,
        )

        cheek_color = (255, 200, 200)
        draw.ellipse([x - 25, y + 5, x - 15, y + 15], fill=cheek_color)
        draw.ellipse([x + 15, y + 5, x + 25, y + 15], fill=cheek_color)

    def draw_face_surprise(self, draw, x, y):
        eye_color = (0, 0, 0)
        eye_radius = 10

        draw.ellipse([x - 25, y - 10, x - 15, y], fill=eye_color)
        draw.ellipse([x + 15, y - 10, x + 25, y], fill=eye_color)

        mouth_color = (255, 100, 100)
        draw.ellipse([x - 10, y + 20, x + 10, y + 30], fill=mouth_color)

    def draw_face_sleeping(self, draw, x, y):
        eye_color = (100, 100, 100)

        draw.line([x - 20, y, x - 10, y], fill=eye_color, width=3)
        draw.line([x + 10, y, x + 20, y], fill=eye_color, width=3)

        mouth_color = (200, 150, 150)
        draw.line([x - 10, y + 15, x + 10, y + 15], fill=mouth_color, width=2)

    def draw_hair(self, draw, x, y, sway=0):
        hair_color = (0, 0, 0)
        hair_highlight = (50, 50, 50)

        hair_points = [
            (x - 40, y - 40),
            (x - 50 + sway, y - 60),
            (x - 30 + sway, y - 80),
            (x, y - 90),
            (x + 30 - sway, y - 80),
            (x + 50 - sway, y - 60),
            (x + 40, y - 40),
            (x + 30, y - 30),
            (x, y - 20),
            (x - 30, y - 30),
        ]

        draw.polygon(hair_points, fill=hair_color)

        twin_color = (100, 0, 100)
        draw.ellipse([x - 45, y - 85, x - 35, y - 75], fill=twin_color)
        draw.ellipse([x + 35, y - 85, x + 45, y - 75], fill=twin_color)

    def draw_clothes(self, draw, x, y, sway=0):
        dress_color = (150, 50, 150)
        dress_highlight = (180, 80, 180)

        dress_points = [
            (x - 30, y),
            (x - 40 + sway, y + 40),
            (x - 50 + sway, y + 80),
            (x + 50 - sway, y + 80),
            (x + 40 - sway, y + 40),
            (x + 30, y),
        ]

        draw.polygon(dress_points, fill=dress_color)

        ribbon_color = (255, 100, 100)
        draw.ellipse([x - 15, y - 10, x - 5, y], fill=ribbon_color)
        draw.ellipse([x + 5, y - 10, x + 15, y], fill=ribbon_color)

        draw.line([x - 10, y, x - 10, y + 20], fill=ribbon_color, width=3)
        draw.line([x + 10, y, x + 10, y + 20], fill=ribbon_color, width=3)

    def get_sprite(self, state):
        return self.images.get(state, self.images["idle"])
