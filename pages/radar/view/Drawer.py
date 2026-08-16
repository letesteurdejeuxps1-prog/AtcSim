import pygame

from pages.radar.data.aircraft_data.Aircraft import Aircraft
from pages.radar.data.airspace_data.Point import Point
from pages.radar.helpers.conversion_helper import world_to_screen_x, world_to_screen_y
from pages.radar.view.Camera import Camera
from pages.radar.view.menus.GenericButton import GenericButton
from pages.radar.view.menus.MainMenu import MainMenu


class Drawer:
    icon_file_folder = "pages\\radar\\medias"
    icon_file_format = ".png"
    point_color: str = "W"
    color_default: tuple[int, int, int] = (255, 255, 255)

    font_size: int = 14

    label_offset_y = 2

    def __init__(self, surface: pygame.Surface, root_directory: str, camera: Camera):
        self.surface = surface
        self.root_directory = root_directory
        self.camera = camera
        self.font = pygame.font.SysFont("consolas", self.font_size)

    def draw_line_radar(
            self,
            start_x: int | float,
            start_y: int | float,
            end_x: int | float,
            end_y: int | float,
            color: tuple[int, int, int],
            width: int = 2
    ):
        sx = int(world_to_screen_x(start_x, self.camera.cam_offset_x, self.camera.zoom))
        sy = int(world_to_screen_y(start_y, self.camera.cam_offset_y, self.camera.zoom))
        ex = int(world_to_screen_x(end_x, self.camera.cam_offset_x, self.camera.zoom))
        ey = int(world_to_screen_y(end_y, self.camera.cam_offset_y, self.camera.zoom))

        pygame.draw.line(
            self.surface,
            color,
            (sx, sy),
            (ex, ey),
            width
        )

    def draw_line_screen(
            self,
            start_x: int,
            start_y: int,
            end_x: int,
            end_y: int,
            color: tuple[int, int, int],
            width: int = 1
    ):
        pygame.draw.line(
            self.surface,
            color,
            (start_x, start_y),
            (end_x, end_y),
            width
        )

    def draw_rect_centered_radar(
            self,
            pos_x: int | float,
            pos_y: int | float,
            width: int | float,
            height: int | float,
            color: tuple[int, int, int],
            border: int = 1
    ):
        start_x = int(world_to_screen_x(pos_x, self.camera.cam_offset_x, self.camera.zoom))
        start_y = int(world_to_screen_y(pos_y, self.camera.cam_offset_y, self.camera.zoom))

        rect = pygame.Rect(0, 0, width, height)
        rect.center = start_x, start_y
        pygame.draw.rect(
            self.surface,
            color,
            rect,
            border
        )

    def draw_fixed_rect_from_rect_radar(
            self,
            rect: pygame.Rect,
            color: tuple[int, int, int],
            border_width = 0
    ):
        pygame.draw.rect(
            self.surface,
            color,
            rect,
            border_width
        )

    def draw_area(self, coords):

        if len(coords) < 2:
            return

        for start, end in zip(coords, coords[1:]):
            self.draw_line_radar(
                start[0],
                start[1],
                end[0],
                end[1],
                (155, 155, 155)
            )

        self.draw_line_radar(
            coords[-1][0],
            coords[-1][1],
            coords[0][0],
            coords[0][1],
            (155, 155, 155)
        )

    def draw_acft(self, acft: Aircraft):

        # Acft body
        self.draw_rect_centered_radar(
            acft.pos_x,
            acft.pos_y,
            acft.body_width,
            acft.body_height,
            acft.color_body
        )

        # Acft PRL
        self.draw_line_radar(
            acft.pos_x,
            acft.pos_y,
            acft.prl_end_x,
            acft.prl_end_y,
            acft.color_prl
        )

        self.draw_aircraft_label(acft)

    def draw_aircraft_label(self, acft: Aircraft):

        label = acft.label

        label.update_layout(
            acft,
            self.camera,
            self.font
        )

        # --------------------------------------------------------------
        # Aircraft position
        # --------------------------------------------------------------

        aircraft_x = int(
            world_to_screen_x(
                acft.pos_x,
                self.camera.cam_offset_x,
                self.camera.zoom
            )
        )

        aircraft_y = int(
            world_to_screen_y(
                acft.pos_y,
                self.camera.cam_offset_y,
                self.camera.zoom
            )
        )

        # --------------------------------------------------------------
        # Leader line
        # --------------------------------------------------------------

        connection_x, connection_y = label.get_connection_point(
            acft,
            self.camera
        )

        self.draw_line_screen(
            aircraft_x,
            aircraft_y,
            connection_x,
            connection_y,
            (255, 255, 255),
            1
        )

        # --------------------------------------------------------------
        # Draw fields
        # --------------------------------------------------------------

        for line in label.lines:

            for field_name, field_value in line:
                rect = label.field_rects[field_name]

                text_surface = self.font.render(
                    str(field_value),
                    True,
                    (255, 255, 255)
                )

                self.surface.blit(
                    text_surface,
                    rect.topleft
                )

    def draw_icon_radar(self, point: Point, should_display_name: bool = False):
        if point.pygame_img is None:
            point.set_image_file(
                self.root_directory,
                self.icon_file_folder,
                self.point_color,
                self.icon_file_format,
            )

        if isinstance(point.pygame_img, pygame.Surface):
            pos_x = int(world_to_screen_x(point.pos_x, self.camera.cam_offset_x, self.camera.zoom))
            pos_y = int(world_to_screen_y(point.pos_y, self.camera.cam_offset_y, self.camera.zoom))
            rect = point.pygame_img.get_rect(center=(pos_x, pos_y))
            self.surface.blit(point.pygame_img, rect)

        if should_display_name:
            txt = point.abbreviation.upper()
            if self.point_color == 'W':
                color = (255, 255, 255)
            elif self.point_color == 'B':
                color = (0, 0, 0)
            else:
                color = self.color_default
            pos_x = int(world_to_screen_x(point.pos_x, self.camera.cam_offset_x, self.camera.zoom))
            pos_y = int(world_to_screen_y(point.pos_y, self.camera.cam_offset_y, self.camera.zoom))
            txt_surface = self.font.render(txt, True, color)
            txt_rect = txt_surface.get_rect()
            txt_rect.centerx = pos_x
            if isinstance(point.pygame_img, pygame.Surface):
                txt_rect.top = pos_y + point.pygame_img.get_height() // 2 + self.label_offset_y

            self.surface.blit(txt_surface, txt_rect)

    def draw_main_menu(self, main_menu: MainMenu):
        # Draw BG
        self.draw_fixed_rect_from_rect_radar(main_menu.rect, main_menu.bg_color)

        # Draw buttons
        for button in main_menu.button_list:
            self.draw_menu_button(button)

    def draw_menu_button(self, button: GenericButton):
        # Draw BG
        self.draw_fixed_rect_from_rect_radar(button.rect, button.get_bg_color())
        self.draw_fixed_rect_from_rect_radar(button.rect, button.get_margin_color(), 3)

        # Draw text
        text_surface = self.font.render(
            str(button.txt),
            True,
            button.txt_color
        )
        mid_x = button.rect.centerx
        mid_y = button.rect.centery
        rect = text_surface.get_rect(center=(mid_x, mid_y))
        self.surface.blit(text_surface, rect)
