import pygame

from pages.radar.helpers.conversion_helper import world_to_screen_x, world_to_screen_y
from pages.radar.view.Camera import Camera


class Drawer:
    def __init__(self, surface: pygame.Surface, root_directory: str, camera: Camera):
        self.surface = surface
        self.root_directory = root_directory
        self.camera = camera

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