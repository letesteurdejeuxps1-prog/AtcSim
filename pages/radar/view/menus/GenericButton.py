import pygame
from typing import Callable


class GenericButton:

    def __init__(
            self,
            pos_x: int,
            pos_y: int,
            txt: str,
            width: int = 0,
            height: int = 0,
            action: Callable[[], None] | None = None
    ):
        self.pos_x = pos_x
        self.pos_y = pos_y

        # Draw data
        self.width = width
        self.height = height

        # Colors
        self.bg_color = (100, 100, 100)
        self.hover_bg_color = (130, 130, 130)
        self.pressed_bg_color = (70, 70, 70)

        self.margin_color = (255, 255, 255)
        self.hover_margin_color = (255, 255, 0)
        self.pressed_margin_color = (255, 255, 255)

        self.txt_color = (255, 255, 255)

        # Content
        self.txt = txt

        # Action
        self.action = action

        # State
        self.hovered = False
        self.pressed = False

        # Object
        self.rect = pygame.Rect(
            self.pos_x,
            self.pos_y,
            self.width,
            self.height
        )

    def update_hover(self, mouse_pos: tuple[int, int]):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def mouse_down(self, mouse_pos: tuple[int, int]):
        if self.rect.collidepoint(mouse_pos):
            self.pressed = True

    def mouse_up(self, mouse_pos: tuple[int, int]):
        was_pressed = self.pressed
        self.pressed = False

        if was_pressed and self.rect.collidepoint(mouse_pos):
            self.click()

    def click(self):
        if self.action is not None:
            self.action()

    def get_bg_color(self):
        if self.pressed:
            return self.pressed_bg_color

        if self.hovered:
            return self.hover_bg_color

        return self.bg_color

    def get_margin_color(self):
        if self.pressed:
            return self.pressed_margin_color

        if self.hovered:
            return self.hover_margin_color

        return self.margin_color