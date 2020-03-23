import pygame
import json
import os
import time


class Config:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.keypos = []
        self.buttons = []
        self.joystick = -1
        self.file_name = ""

    def __get_int(self, val, fallback: int):
        try:
            return int(val)
        except (ValueError, TypeError):
            print("{} is an invalid int".format(val))
            return 0

    def save(self):
        with open(self.file_name, "w") as f:
            json.dump({
                "x": self.x,
                "y": self.y,
                "keypos": self.keypos,
                "joystick": self.joystick,
                "buttons": self.buttons
            }, f)

    @classmethod
    def load_config(cls, file_name: str = "config.json"):
        if not os.path.isfile(file_name):
            print("Not valid file")
            return None
        with open(file_name, "r") as f:
            dat = json.load(f)
        c = cls()
        c.x = c.__get_int(dat.get("x"), 100)
        c.y = c.__get_int(dat.get("y"), 100)
        c.keypos = dat.get("keypos", [])
        c.joystick = c.__get_int(dat.get("joystick"), -1)
        c.file_name = file_name
        c.buttons = dat.get("buttons", [])
        return c


class BMSKPS:

    def __init__(self, config: Config):
        # Class var
        self.config = config
        self.running = False
        self.ready = False
        self.joystick = None

        # PyGame vars
        self.screen = None
        self.clock = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def render(self):
        self.screen.fill((0, 0, 255))

        for button, i in enumerate(self.config.buttons):
            if self.joystick.get_button(button):    # If button is pressed
                pygame.draw.rect(
                    self.screen,
                    (100, 100, 100) if i % 2 == 0 else (100, 100, 100),
                    self.config.keypos[i]
                )
            else:                                   # Not pressed
                pygame.draw.rect(
                    self.screen,
                    (255, 255, 255) if i % 2 == 0 else (0, 0, 0),
                    self.config.keypos[i]
                )

        pygame.display.flip()

    def run(self):
        # Setup pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.config.x, self.config.y))
        pygame.display.set_caption("BMS-KPS")
        self.clock = pygame.time.Clock()
        pygame.joystick.init()

        if config.joystick == -1:
            print("Select a joystick: ")
            for joystick_id in range(pygame.joystick.get_count()):
                joystick = pygame.joystick.Joystick(joystick_id)
                joystick.init()
                print("{}. {}".format(joystick_id, joystick.get_name()))
            while True:
                try:
                    jsid = int(input("ID: "))
                    break
                except ValueError:
                    pass
            self.config.joystick = jsid
            self.config.save()
        self.joystick = pygame.joystick.Joystick(self.config.joystick)
        self.joystick.init()

        # Begin loop
        self.running = True

        try:
            while self.running:
                self.handle_events()

                # Wait for window to be created
                if not self.ready and self.clock.get_fps() >= 1:
                    self.ready = True

                if self.ready:      # If ready to be drawn to window
                    self.render()   # Render frame

                # Tick fps
                self.clock.tick(60)
        except KeyboardInterrupt:
            self.running = False


if __name__ == "__main__":
    config = Config.load_config()
    BMSKPS(config).run()
