import pathlib
import pygame

from pages.Variables import Variables
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
        self.airspace = Airspace()
        self.aircraft_handler = AircraftHandler()
        self.camera = Camera()
        self.screen = Screen(self.main_surface, self.root_directory, self.camera)

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
            self.screen.fill_bg()
            for event in pygame.event.get():
                self.handle_event(event)
            self.aircraft_handler.update()
            self.screen.update(
                self.airspace,
                self.aircraft_handler
            )
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

    """
    EVENTS HANDLING
    """

    def handle_event(self, event: pygame.event.Event):
        # Quit event
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            self.is_running = False
        # MOUSEWHEEL SCROLL
        elif event.type == pygame.MOUSEWHEEL:
            self.handle_event_scroll(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_event_mouseclick(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_event_mouseclick_off()
        elif event.type == pygame.MOUSEMOTION:
            self.handle_mouse_motion(event)

    def handle_event_scroll(self, event: pygame.event.Event):

        mouse_x, mouse_y = pygame.mouse.get_pos()

        world_x = (mouse_x + self.camera.cam_offset_x) / self.camera.zoom
        world_y = -(mouse_y + self.camera.cam_offset_y) / self.camera.zoom

        zoom_factor = 1.1 if event.y > 0 else 0.9

        self.camera.zoom *= zoom_factor

        self.camera.zoom = max(0.1, min(self.camera.zoom, 500))

        self.camera.cam_offset_x = world_x * self.camera.zoom - mouse_x
        self.camera.cam_offset_y = -world_y * self.camera.zoom - mouse_y

    def handle_event_mouseclick(self, event: pygame.event.Event):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.button == 1:
            # Left click
            self.left_click_on = True
        if event.button == 2:
            # Middle click
            self.middle_click_on = True
        if event.button == 3:
            # Right click
            self.right_click_on = True

    def handle_event_mouseclick_off(self):
        self.left_click_on = False
        self.middle_click_on = False
        self.right_click_on = False

    def handle_mouse_motion(self, event):
        if self.middle_click_on or self.right_click_on:
            self.handle_event_mouse_middle_click_drag(event)

    def handle_event_mouse_middle_click_drag(self, event):
        if isinstance(event.rel, tuple) and len(event.rel) == 2:
            self.camera.cam_offset_x -= event.rel[0]
            self.camera.cam_offset_y -= event.rel[1]