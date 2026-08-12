import pygame

from pages.radar.data.AircraftHandler import AircraftHandler
from pages.radar.data.Airspace import Airspace
from pages.radar.view.Camera import Camera
from pages.radar.view.Drawer import Drawer


class Screen:

    radar_color_bg: tuple[int, int, int] = (0, 0, 0)

    def __init__(self, surface: pygame.Surface, root_directory: str, camera: Camera):
        self.surface = surface
        self.root_directory = root_directory
        self.camera = camera
        self.zoom = 1
        self.drawer = Drawer(self.surface, self.root_directory, self.camera)
        self.cam_offset_x = 0
        self.cam_offset_y = 0

    def update(self, asp: Airspace, acft_handler: AircraftHandler):
        self.draw_airspace(asp)
        self.draw_aerodromes()
        self.draw_acft()
        self.draw_qdm()
        pygame.display.flip()

    def fill_bg(self):
        self.surface.fill(self.radar_color_bg)

    def draw_airspace(self, asp: Airspace):
        for area in asp.areas:
            self.drawer.draw_area(area.coordinates_converted)

    def draw_aerodromes(self):
        pass

    def draw_acft(self):
        pass

    def draw_qdm(self):
        pass

