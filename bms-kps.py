import pygame
import json
import os
import time
import math
import sys


class Config:

    def __init__(self):
        self.window_x = 0
        self.window_y = 0
        self.window_bg = []
        self.joystick_id = -1
        self.keys = []
        self.kps_enabled = False
        self.kps_x = 0
        self.kps_y = 0
        self.kps_font = ""
        self.kps_size = 30
        self.kps_color = 255

    def __get_int(self, val, fallback: int):
        try:
            return int(val)
        except (ValueError, TypeError):
            print("{} is an invalid int".format(val))
            return fallback

    @classmethod
    def load_config(cls, file_name: str):
        if not os.path.isfile(file_name):
            print("Not valid file")
            return None
        with open(file_name, "r") as f:
            dat = json.load(f)

        c = cls()
        c.window_x = c.__get_int(dat.get("window", {}).get("x", 0), 100)
        c.window_y = c.__get_int(dat.get("window", {}).get("y", 0), 100)
        c.window_bg = dat.get("window", {}).get("bg", [])
        c.joystick_id = c.__get_int(dat.get("joystick_id", -1), -1)
        c.keys = dat.get("keys", [])
        kps = dat.get("kps", {})
        c.kps_enabled = kps.get("enabled", False)
        c.kps_x = kps.get("x", 0)
        c.kps_y = kps.get("y", 0)
        c.kps_font = kps.get("font", "")
        c.kps_size = c.__get_int(kps.get("size", 30), 30)
        c.kps_color = c.__get_int(kps.get("color", 255), 255)
        return c


class BMSKPS:

    def __init__(self, config: Config):
        # Class var
        self.config = config
        self.running = False
        self.joystick = None
        self.key_presses = []
        self.font = None
        self.skip_joycheck = True

        # PyGame vars
        self.screen = None
        self.clock = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.JOYBUTTONDOWN:
                self.key_presses.append(time.time())

    def draw_rect(self, color: int, x: int, y: int, w: int, h: int):
        pygame.draw.rect(
            self.screen,
            (color, color, color),
            (x, y, w, h)
        )

    def draw_circle(self, color: int, x: int, y: int, radius: int, angle: int):
        pygame.draw.circle(
            self.screen,
            (color, color, color),
            (x, y), radius, 2
        )
        pygame.draw.line(
            self.screen,
            (color, color, color),
            (x, y), (x + (radius * math.cos(angle * math.pi / 180)), y + (radius * math.sin(angle * math.pi / 180))), 2
        )

    def render(self):
        self.screen.fill(self.config.window_bg)

        for i, button in enumerate(self.config.keys):
            if button[1] == 0:
                self.draw_rect(
                    128 if self.joystick.get_button(button[0]) else button[6],
                    button[2],
                    button[3],
                    button[4],
                    button[5]
                )
            elif button[1] == 1:
                self.draw_circle(button[6], button[2], button[3], button[4], self.joystick.get_axis(button[0]) * 360)

        for i, kt in enumerate(self.key_presses):
            if (time.time() - kt) > 1:
                del self.key_presses[i]

        if self.config.kps_enabled:
            text = "{} kps".format(len(self.key_presses))
            self.screen.blit(
                self.font.render(text, False, (self.config.kps_color, self.config.kps_color, self.config.kps_color)),
                (self.config.kps_x, self.config.kps_y)
            )

        pygame.display.flip()

    def quit(self):
        pygame.font.quit()
        pygame.joystick.quit()
        pygame.quit()

    def wait_for_ready(self):
        while True:
            self.handle_events()
            if self.clock.get_fps() >= 1:
                break
            self.clock.tick(60)
        print("Ready")

    def run(self):
        # Setup pygame
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((self.config.window_x, self.config.window_y))
        pygame.display.set_caption("BMS-KPS")
        self.clock = pygame.time.Clock()
        pygame.joystick.init()
        self.font = pygame.font.SysFont("arial", self.config.kps_size)

        if self.config.joystick_id < 0:
            print("Set a joystick in the config: ")
            for joystick_id in range(pygame.joystick.get_count()):
                joystick = pygame.joystick.Joystick(joystick_id)
                joystick.init()
                print("{}. {}".format(joystick_id, joystick.get_name()))
                self.quit()
            return

        try:
            self.joystick = pygame.joystick.Joystick(self.config.joystick_id)
            self.joystick.init()
        except pygame.error:
            print("Invalid joystick")
            if not self.skip_joycheck:
                self.quit()
                return

        # Begin loop
        self.running = True

        # Wait for ready
        self.wait_for_ready()

        try:
            while self.running:
                self.handle_events()
                self.render()   # Render frame

                # Tick fps
                self.clock.tick(60)
        except KeyboardInterrupt:
            self.running = False


if __name__ == "__main__":
    _config = Config.load_config()
    BMSKPS(_config).run()
