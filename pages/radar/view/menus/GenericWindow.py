import pygame

from pages.radar.view.menus.GenericButton import GenericButton


class GenericWindow:

    title_bar_height = 25
    close_button_width = 25

    def __init__(
            self,
            pos_x: int,
            pos_y: int,
            width: int,
            height: int,
            title: str = ""
    ):
        # --------------------------------------------------------------
        # Position / dimensions
        # --------------------------------------------------------------

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.width = width
        self.height = height

        self.title = title

        # --------------------------------------------------------------
        # Colors
        # --------------------------------------------------------------

        self.bg_color = (40, 40, 40)
        self.title_bar_color = (60, 60, 60)
        self.border_color = (255, 255, 255)
        self.title_color = (255, 255, 255)

        # --------------------------------------------------------------
        # State
        # --------------------------------------------------------------

        self.visible = True

        self.dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        # --------------------------------------------------------------
        # Window rectangle
        # --------------------------------------------------------------

        self.rect = pygame.Rect(
            self.pos_x,
            self.pos_y,
            self.width,
            self.height
        )

        # --------------------------------------------------------------
        # Close button
        # --------------------------------------------------------------

        self.close_button = GenericButton(
            self.pos_x + self.width - self.close_button_width,
            self.pos_y,
            "X",
            self.close_button_width,
            self.title_bar_height,
            self.close
        )

        # --------------------------------------------------------------
        # Child buttons
        # --------------------------------------------------------------

        self.button_list: list[GenericButton] = []

    # ==================================================================
    # Position
    # ==================================================================

    def update_rect(self):
        self.rect.topleft = (
            self.pos_x,
            self.pos_y
        )

        self.close_button.rect.topleft = (
            self.pos_x + self.width - self.close_button_width,
            self.pos_y
        )

    # ==================================================================
    # Visibility
    # ==================================================================

    def open(self):
        self.visible = True

    def close(self):
        self.visible = False
        self.dragging = False

    # ==================================================================
    # Drawing
    # ==================================================================

    def draw(self, surface: pygame.Surface, font: pygame.font.Font):

        if not self.visible:
            return

        # Window background
        pygame.draw.rect(
            surface,
            self.bg_color,
            self.rect
        )

        # Window border
        pygame.draw.rect(
            surface,
            self.border_color,
            self.rect,
            2
        )

        # Title bar
        title_rect = pygame.Rect(
            self.pos_x,
            self.pos_y,
            self.width,
            self.title_bar_height
        )

        pygame.draw.rect(
            surface,
            self.title_bar_color,
            title_rect
        )

        # Title
        title_surface = font.render(
            self.title,
            True,
            self.title_color
        )

        title_text_rect = title_surface.get_rect(
            midleft=(
                self.pos_x + 8,
                self.pos_y + self.title_bar_height // 2
            )
        )

        surface.blit(
            title_surface,
            title_text_rect
        )

        # Close button
        self.draw_button(
            surface,
            font,
            self.close_button
        )

        # Other buttons
        for button in self.button_list:
            self.draw_button(
                surface,
                font,
                button
            )

    @staticmethod
    def draw_button(
            surface: pygame.Surface,
            font: pygame.font.Font,
            button: GenericButton
    ):

        pygame.draw.rect(
            surface,
            button.get_bg_color(),
            button.rect
        )

        pygame.draw.rect(
            surface,
            button.get_margin_color(),
            button.rect,
            2
        )

        text_surface = font.render(
            str(button.txt),
            True,
            button.txt_color
        )

        text_rect = text_surface.get_rect(
            center=button.rect.center
        )

        surface.blit(
            text_surface,
            text_rect
        )

    # ==================================================================
    # Mouse interaction
    # ==================================================================

    def update_mouse(self, mouse_pos: tuple[int, int]):

        if not self.visible:
            return

        self.close_button.update_hover(mouse_pos)

        for button in self.button_list:
            button.update_hover(mouse_pos)

    def mouse_down(self, mouse_pos: tuple[int, int]) -> bool:

        if not self.visible:
            return False

        # --------------------------------------------------------------
        # Close button
        # --------------------------------------------------------------

        if self.close_button.rect.collidepoint(mouse_pos):
            self.close_button.mouse_down(mouse_pos)
            return True

        # --------------------------------------------------------------
        # Child buttons
        # --------------------------------------------------------------

        for button in self.button_list:
            if button.rect.collidepoint(mouse_pos):
                button.mouse_down(mouse_pos)
                return True

        # --------------------------------------------------------------
        # Window title bar -> start dragging
        # --------------------------------------------------------------

        title_bar_rect = pygame.Rect(
            self.pos_x,
            self.pos_y,
            self.width,
            self.title_bar_height
        )

        if title_bar_rect.collidepoint(mouse_pos):

            self.dragging = True

            self.drag_offset_x = (
                mouse_pos[0] - self.pos_x
            )

            self.drag_offset_y = (
                mouse_pos[1] - self.pos_y
            )

            return True

        # --------------------------------------------------------------
        # Window itself
        # --------------------------------------------------------------

        if self.rect.collidepoint(mouse_pos):
            return True

        return False

    def mouse_drag(self, mouse_pos: tuple[int, int]):

        if not self.visible or not self.dragging:
            return

        self.pos_x = (
            mouse_pos[0] - self.drag_offset_x
        )

        self.pos_y = (
            mouse_pos[1] - self.drag_offset_y
        )

        self.update_rect()

    def mouse_up(self, mouse_pos: tuple[int, int]):

        if not self.visible:
            return

        self.close_button.mouse_up(mouse_pos)

        for button in self.button_list:
            button.mouse_up(mouse_pos)

        self.dragging = False