import pygame

from pages.radar.data.airspace_data.Point import Point
from pages.radar.helpers.conversion_helper import world_to_screen_x, world_to_screen_y
from pages.radar.view.Camera import Camera


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

    def draw_line(
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

    def draw_area(self, coords):

        if len(coords) < 2:
            return

        for start, end in zip(coords, coords[1:]):
            self.draw_line(
                start[0],
                start[1],
                end[0],
                end[1],
                (155, 155, 155)
            )

        self.draw_line(
            coords[-1][0],
            coords[-1][1],
            coords[0][0],
            coords[0][1],
            (155, 155, 155)
        )

    def draw_icon(self, point: Point, should_display_name: bool = False):
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
            txt_rect.top = pos_y + point.pygame_img.get_height() // 2 + self.label_offset_y

            self.surface.blit(txt_surface, txt_rect)
