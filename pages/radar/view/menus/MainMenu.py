import pygame

from pages.radar.view.menus.ClickableButton import ClickableButton
from pages.radar.view.menus.GenericButton import GenericButton


class MainMenu:
    max_height = 150

    def __init__(self, width: int):
        # Positions
        self.pos_x = 0
        self.pos_y = 0

        # Draw data
        self.padding_top = 10
        self.padding_bottom = 10
        self.padding_left = 25
        self.padding_right = 25
        self.width = width
        self.height = 50

        # Colors
        self.bg_color = (50, 50, 50)
        self.margin_bottom_color = (255, 255, 255)

        # Content
        self.button_list = []
        # TODO : Change following function between populate_button_list_display_flex or populate_button_list to set the menu layout
        self.populate_button_list()

        # Object
        self.rect = pygame.Rect(
            self.pos_x,
            self.pos_y,
            self.width,
            self.height
        )

    def populate_button_list(self):
        button_height = self.height - self.padding_top - self.padding_bottom
        button_x_pos = self.padding_left
        button_y_pos = self.padding_top

        self.button_list = []

        for txt, button_class, width, action in self.get_buttons_list():
            button = button_class(
                button_x_pos,
                button_y_pos,
                txt,
                width,
                button_height,
                action
            )

            self.button_list.append(button)

            button_x_pos += button.width + self.padding_right

    def populate_button_list_display_flex(self):
        button_height = self.height - self.padding_top - self.padding_bottom

        button_definitions = self.get_buttons_list()

        self.button_list = []

        # Create the actual button objects
        for txt, button_class, width, action in button_definitions:
            button = button_class(
                0,
                self.padding_top,
                txt,
                width,
                button_height,
                action
            )

            self.button_list.append(button)

        # Calculate total width occupied by buttons
        total_button_width = sum(
            button.width
            for button in self.button_list
        )

        # Remaining space available for gaps
        available_width = (
                self.width
                - self.padding_left
                - self.padding_right
                - total_button_width
        )

        # Number of gaps between buttons
        number_of_gaps = len(self.button_list) - 1

        if number_of_gaps > 0:
            spacing = available_width / number_of_gaps
        else:
            spacing = 0

        # Position buttons
        x = self.padding_left

        for button in self.button_list:
            button.pos_x = int(x)
            button.rect.x = button.pos_x

            x += button.width + spacing

    def update_mouse(self, mouse_pos: tuple[int, int]):
        for button in self.button_list:
            button.update_hover(mouse_pos)

    def mouse_down(self, mouse_pos: tuple[int, int]):
        for button in self.button_list:
            button.mouse_down(mouse_pos)

    def mouse_up(self, mouse_pos: tuple[int, int]):
        for button in self.button_list:
            button.mouse_up(mouse_pos)

    # Button actions
    def get_buttons_list(self):
        return [
            (
                "Test",
                GenericButton,
                150,
                self.test_button_action_1
            ),
            (
                "Test 2",
                ClickableButton,
                200,
                self.test_button_action_2
            ),
        ]

    def test_button_action_1(self):
        self.bg_color = (255, 50, 50)

    def test_button_action_2(self):
        if self.bg_color == (50, 50, 50):
            self.bg_color = (100, 100, 100)
        else:
            self.bg_color = (50, 50, 50)
