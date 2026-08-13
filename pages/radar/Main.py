import pathlib
import pygame

from pages.Variables import Variables
from pages.radar.EventHandler import EventHandler
from pages.radar.data.aircraft_data.AircraftHandler import AircraftHandler
from pages.radar.data.Airspace import Airspace
from pages.radar.helpers.Test import Test
from pages.radar.view.Camera import Camera
from pages.radar.view.Screen import Screen


class Main:

    def __init__(self, v: Variables, working_dir: str) -> None:
        # Passed Variables
        self.variables = v
        self.root_directory = working_dir

        # Set up internal vars
        self.is_running = True
        self.root_directory = working_dir
        self.path_root = str(pathlib.Path().resolve())
        # General variables
        self.path_airspace_file: str = 'ESSH.json'
        self.path_airspace_folder: str = 'airspaces'

        # click variables
        self.left_click_on = False
        self.right_click_on = False
        self.middle_click_on = False

        # Init PyGame and other stuff
        pygame.init()
        pygame.mixer.init()
        self.font = pygame.font.SysFont("consolas", 14)
        info = pygame.display.Info()
        self.variables.display_width = info.current_w
        self.variables.display_height = info.current_h
        self.main_surface = pygame.display.set_mode((self.variables.display_width, self.variables.display_height))
        self.main_clock: pygame.time.Clock = pygame.time.Clock()

        # Init objects
        self.event_handler = EventHandler(self)
        self.airspace = Airspace()
        self.aircraft_handler = AircraftHandler()
        self.camera = Camera()
        # TODO Remove next line after debug
        self.testing_object = Test()
        self.screen = Screen(self.main_surface, self.root_directory, self.camera)

        # Init function
        self.init()

    def test_init(self):
        # TODO: REMOVE FUNCTION AFTER DEBUG
        acfts = self.testing_object.load_acft(self.root_directory, self.airspace.origin_lon, self.airspace.origin_lat)
        self.aircraft_handler.testing_populate_list(acfts)

    def init(self):
        pygame.display.set_caption(self.variables.game_caption)
        self.variables.display_width_half = self.variables.display_width // 2
        self.variables.display_height_half = self.variables.display_height // 2
        self.load_airspace()
        self.camera.set_center(
            self.variables.display_width,
            self.variables.display_height
        )
        # TODO: REMOVE NEXT LINE AFTER DEBUG
        self.test_init()

    def run(self):
        while self.is_running:
            self.screen.fill_bg()
            for event in pygame.event.get():
                self.event_handler.handle_event(event)

            elapsed_time = self.main_clock.tick(self.variables.display_fps)

            self.aircraft_handler.update(elapsed_time)
            self.screen.update(
                self.airspace,
                self.aircraft_handler
            )
            pygame.display.flip()


        pygame.quit()

    def load_airspace(self):
        airspace_file_path = "{}\\{}\\{}".format(
            self.path_root,
            self.path_airspace_folder,
            self.path_airspace_file
        )
        self.airspace.load(airspace_file_path)

