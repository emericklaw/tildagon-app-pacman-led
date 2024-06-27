import app
from app_components import Menu, Notification, clear_background
import machine
import utime
from tildagon import Pin as ePin
import settings
from system.hexpansion.config import HexpansionConfig
from app_components import layout as layout

main_menu_items = [
    "Power",
    "Slot",
    "About",
]

power_menu_items = ["On", "Off"]


class Pacman(app.App):
    def __init__(self):
        # Menu setup
        self.menu = None
        self.current_menu = None
        self.set_menu("main")

        # Notification setup
        self.notification = None

        # Main app setup
        self.power = True

        self.pins = {
            "eye": None,
            "dot_1": None,
            "dot_2": None,
            "dot_3": None,
        }

        self._init_pins()
        self.frame = 1
        self.last_update = utime.ticks_ms()

    def _init_pins(self):
        self.hexpansion_config = HexpansionConfig(settings.get("pacmanled.slot", 1))
        self.pins["eye"] = self.hexpansion_config.ls_pin[0]
        self.pins["eye"].init(self.pins["eye"].OUT)
        self.pins["dot_1"] = self.hexpansion_config.ls_pin[3]
        self.pins["dot_1"].init(self.pins["dot_1"].OUT)
        self.pins["dot_2"] = self.hexpansion_config.ls_pin[2]
        self.pins["dot_2"].init(self.pins["dot_2"].OUT)
        self.pins["dot_3"] = self.hexpansion_config.ls_pin[1]
        self.pins["dot_3"].init(self.pins["dot_3"].OUT)
        self.pins["dot_1"].value(1)
        self.pins["dot_2"].value(1)
        self.pins["dot_3"].value(1)
        self.pins["eye"].value(0)

    def set_slot(self, slot):
        slot = int(slot)
        settings.set("pacmanled.slot", slot)
        settings.save()
        self.pins["dot_1"].value(0)
        self.pins["dot_2"].value(0)
        self.pins["dot_3"].value(0)
        self.pins["eye"].value(0)
        self._init_pins()

    def back_handler(self):
        # If in the topmost menu, minimize, otherwise move one menu up.
        if self.current_menu == "main":
            self.minimise()
        else:
            self.set_menu("main")

    def select_handler(self, item, idx):
        # If Power or Preset item selected enter that menu
        if item in main_menu_items:
            self.set_menu(item)
        else:
            if self.current_menu == "Power":
                if item == "On":
                    self.notification = Notification("Power On")
                    self.power = True
                    self.pins["eye"].value(0)
                    self.set_menu("main")
                elif item == "Off":
                    self.notification = Notification("Power Off")
                    self.power = False
                    self.pins["dot_1"].value(1)
                    self.pins["dot_2"].value(1)
                    self.pins["dot_3"].value(1)
                    self.pins["eye"].value(1)
                    self.set_menu("main")
            elif self.current_menu == "Slot":
                if item in ["1", "2", "3", "4", "5", "6"]:
                    self.notification = Notification("Slot=" + item)
                    self.set_slot(item)
                    self.set_menu("main")
            else:
                self.notification = Notification(self.current_menu + "." + item + '"!')

    def set_menu(
        self,
        menu_name: Literal[
            "main",
            "Power",
        ],
    ):
        if self.menu:
            self.menu._cleanup()
        if self.current_menu:
            previous_menu = self.current_menu
        else:
            previous_menu = "Power"
        self.current_menu = menu_name
        if menu_name == "main":
            self.menu = Menu(
                self,
                main_menu_items,
                select_handler=self.select_handler,
                back_handler=self.back_handler,
                position=(main_menu_items).index(previous_menu),
            )
        elif menu_name == "Power":
            self.menu = Menu(
                self,
                power_menu_items,
                select_handler=self.select_handler,
                back_handler=self.back_handler,
                position=0 if self.power else 1,
            )
        elif menu_name == "Slot":
            self.menu = Menu(
                self,
                ["1", "2", "3", "4", "5", "6"],
                select_handler=self.select_handler,
                back_handler=self.back_handler,
                position=settings.get("pacmanled.slot", 1) - 1,
            )
        elif menu_name == "About":
            self.menu = Menu(
                self,
                [
                    "",
                ],
                back_handler=self.back_handler,
            )

    def draw(self, ctx):
        clear_background(ctx)

        self.menu.draw(ctx)

        if self.notification:
            self.notification.draw(ctx)

        if self.current_menu == "About":
            # ctx.font_size = 24
            ctx.save()
            self.about_layout = layout.LinearLayout(
                [
                    layout.TextDisplay("- Version: 0.1.0"),
                    layout.TextDisplay(
                        "Control the LEDs on the Pacman hexpansion created by The Untitled Goose"
                    ),
                ]
            )
            self.about_layout.y_offset = 65
            self.about_layout.x_offset = -60
            self.about_layout.draw(ctx)

            ctx.restore()

    def update(self, delta):
        self.menu.update(delta)
        if self.notification:
            self.notification.update(delta)

    def background_update(self, delta):
        if self.power == True:
            current_time = utime.ticks_ms()
            if utime.ticks_diff(current_time, self.last_update) >= 500:
                self.last_update = current_time
                if self.frame == 1:
                    self.pins["dot_1"].value(1)
                    self.pins["dot_2"].value(1)
                    self.pins["dot_3"].value(0)
                if self.frame == 2:
                    self.pins["dot_1"].value(1)
                    self.pins["dot_2"].value(0)
                    self.pins["dot_3"].value(1)
                if self.frame == 3:
                    self.pins["dot_1"].value(0)
                    self.pins["dot_2"].value(1)
                    self.pins["dot_3"].value(1)
                if self.frame == 4:
                    self.pins["dot_1"].value(1)
                    self.pins["dot_2"].value(1)
                    self.pins["dot_3"].value(1)
                self.frame = self.frame + 1
                if self.frame > 4:
                    self.frame = 1


__app_export__ = Pacman
