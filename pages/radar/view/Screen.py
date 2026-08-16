import pygame

from pages.Variables import Variables
from pages.radar.data.aircraft_data.AircraftHandler import AircraftHandler
from pages.radar.data.Airspace import Airspace
from pages.radar.view.Camera import Camera
from pages.radar.view.Drawer import Drawer
from pages.radar.view.menus.GenericWindow import GenericWindow
from pages.radar.view.menus.MainMenu import MainMenu


class Screen:

    radar_color_bg: tuple[int, int, int] = (0, 0, 0)

    def __init__(self, surface: pygame.Surface, root_directory: str, camera: Camera, variables: Variables):
        self.radar_show_navaids_name = True
        self.surface = surface
        self.variables = variables
        self.root_directory = root_directory
        self.camera = camera
        self.zoom = 1
        self.drawer = Drawer(self.surface, self.root_directory, self.camera)
        self.main_menu = MainMenu(self.variables.display_width)
        self.windows = []
        self.cam_offset_x = 0
        self.cam_offset_y = 0

    def update(self, asp: Airspace, acft_handler: AircraftHandler):
        self.draw_airspace(asp)
        self.draw_aerodromes()
        self.draw_acft(acft_handler)
        self.draw_qdm()
        self.draw_menus()
        self.draw_windows()

    def fill_bg(self):
        self.surface.fill(self.radar_color_bg)

    def draw_airspace(self, asp: Airspace):
        for area in asp.areas:
            self.drawer.draw_area(area.coordinates_converted)
        
        for point in asp.points:
            self.drawer.draw_icon_radar(point, True)

    def draw_aerodromes(self):
        pass

    def draw_acft(self, acft_handler: AircraftHandler):
        for acft in acft_handler.aircraft_list:
            self.drawer.draw_acft(acft)

    def draw_qdm(self):
        pass

    def draw_menus(self):
        self.draw_main_menu()

    def draw_main_menu(self):
        self.drawer.draw_main_menu(self.main_menu)

    def add_window(self, window: GenericWindow):
        self.windows.append(window)

    def draw_windows(self):
        for window in self.windows:
            window.draw(
                self.surface,
                self.drawer.font
            )
