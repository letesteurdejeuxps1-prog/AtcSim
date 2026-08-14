import pygame


class GenericButton:
    def __init__(self, pos_x: int, pos_y: int, txt: str, width: int = 0, height: int = 0):

        self.pos_x = pos_x
        self.pos_y = pos_y

        # Draw data
        self.width = width
        self.height = height

        # Colors
        self.bg_color = (100, 100, 100)
        self.margin_color = (255, 255, 255)
        self.txt_color = (255, 255, 255)

        # Content
        self.txt = txt

        # Object
        self.rect = pygame.Rect(
            self.pos_x,
            self.pos_y,
            self.width,
            self.height
        )