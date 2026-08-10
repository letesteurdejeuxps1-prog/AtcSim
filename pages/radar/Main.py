import pathlib
import pygame

from pages.Variables import Variables
from pages.radar.InputHandler import InputHandler
from pages.radar.data.AircraftHandler import AircraftHandler
from pages.radar.data.Airspace import Airspace
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
        self.path_airspace_file: str = 'horn.json'
        self.path_airspace_folder: str = 'airspaces'

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
        self.airspace = Airspace()
        self.aircraft_handler = AircraftHandler()
        self.screen = Screen()
        self.input_handler = InputHandler()

        # Init function
        self.init()

    def test_init(self):
        # TODO: REMOVE FUNCTION AFTER DEBUG
        pass

    def init(self):
        pygame.display.set_caption(self.variables.game_caption)
        self.variables.display_width_half = self.variables.display_width // 2
        self.variables.display_height_half = self.variables.display_height // 2
        self.load_airspace()
        # TODO: REMOVE NEXT LINE AFTER DEBUG
        self.test_init()

    def run(self):
        while self.is_running:
            for event in pygame.event.get():
                self.handle_event(event)
            self.aircraft_handler.update()
            self.screen.update()
            pygame.display.flip()
            self.main_clock.tick(self.variables.display_fps)

        pygame.quit()

    def load_airspace(self):
        airspace_file_path = "{}\\{}\\{}".format(
            self.path_root,
            self.path_airspace_folder,
            self.path_airspace_file
        )
        self.airspace.load(airspace_file_path)

    def handle_event(self, event: pygame.event.Event):
        # Quit event
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            self.is_running = False

