from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from pages.radar.Main import Main


class EventHandler:

    def __init__(self, parent: "Main"):
        self.parent = parent

    def handle_event(self, event: pygame.event.Event):
        # Quit event
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            self.parent.is_running = False
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

        world_x = (mouse_x + self.parent.camera.cam_offset_x) / self.parent.camera.zoom
        world_y = -(mouse_y + self.parent.camera.cam_offset_y) / self.parent.camera.zoom

        zoom_factor = 1.1 if event.y > 0 else 0.9

        self.parent.camera.zoom *= zoom_factor

        self.parent.camera.zoom = max(0.1, min(self.parent.camera.zoom, 500))

        self.parent.camera.cam_offset_x = world_x * self.parent.camera.zoom - mouse_x
        self.parent.camera.cam_offset_y = -world_y * self.parent.camera.zoom - mouse_y

    def handle_event_mouseclick(self, event: pygame.event.Event):
        mouse_pos = pygame.mouse.get_pos()
        if event.button == 1:
            self.parent.left_click_on = True
            self.parent.screen.main_menu.mouse_down(mouse_pos)

        elif event.button == 2:
            self.parent.middle_click_on = True

        elif event.button == 3:
            self.parent.right_click_on = True

    def handle_event_mouseclick_off(self):
        mouse_pos = pygame.mouse.get_pos()
        self.parent.screen.main_menu.mouse_up(mouse_pos)
        self.parent.left_click_on = False
        self.parent.middle_click_on = False
        self.parent.right_click_on = False

    def handle_mouse_motion(self, event):
        mouse_pos = event.pos
        self.parent.screen.main_menu.update_mouse(mouse_pos)
        if self.parent.middle_click_on or self.parent.right_click_on:
            self.handle_event_mouse_middle_click_drag(event)

    def handle_event_mouse_middle_click_drag(self, event):
        if isinstance(event.rel, tuple) and len(event.rel) == 2:
            self.parent.camera.cam_offset_x -= event.rel[0]
            self.parent.camera.cam_offset_y -= event.rel[1]

