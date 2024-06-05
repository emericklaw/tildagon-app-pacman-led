import app
from app_components import Menu, Notification, clear_background
import machine
import utime
from tildagon import Pin as ePin

main_menu_items = [
    "Power",
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
        self.dot1 = ePin("2_LS_D", machine.Pin.OUT)
        self.dot2 = ePin("2_LS_C", machine.Pin.OUT)
        self.dot3 = ePin("2_LS_B", machine.Pin.OUT)
        self.eye = ePin("2_LS_A", machine.Pin.OUT)
        self.dot1.value(1)
        self.dot2.value(1)
        self.dot3.value(1)
        self.eye.value(0)
        self.frame = 1
        self.last_update = utime.ticks_ms()

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
                    self.eye.value(0)
                    self.set_menu("main")
                elif item == "Off":
                    self.notification = Notification("Power Off")
                    self.power = False
                    self.dot1.value(1)
                    self.dot2.value(1)
                    self.dot3.value(1)
                    self.eye.value(1)
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

    def draw(self, ctx):
        clear_background(ctx)

        self.menu.draw(ctx)

        if self.notification:
            self.notification.draw(ctx)

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
                    self.dot1.value(1)
                    self.dot2.value(1)
                    self.dot3.value(0)
                if self.frame == 2:
                    self.dot1.value(1)
                    self.dot2.value(0)
                    self.dot3.value(1)
                if self.frame == 3:
                    self.dot1.value(0)
                    self.dot2.value(1)
                    self.dot3.value(1)
                if self.frame == 4:
                    self.dot1.value(1)
                    self.dot2.value(1)
                    self.dot3.value(1)
                self.frame = self.frame + 1
                if self.frame > 4:
                    self.frame = 1


__app_export__ = Pacman
