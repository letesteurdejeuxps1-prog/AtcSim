import pygame

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

        #Main menu button
        test_button = GenericButton(button_x_pos, button_y_pos, "Test", 100, button_height)
        self.button_list.append(test_button)
        button_x_pos += test_button.width + self.padding_right

        # TODO remove after DEBUG
        for i in range(4):
            test_btn = GenericButton(button_x_pos, button_y_pos, "Test {}".format(i), 100, button_height)
            button_x_pos += test_btn.width + self.padding_right
            self.button_list.append(test_btn)
