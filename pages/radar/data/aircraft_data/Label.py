import pygame

from pages.radar.helpers.conversion_helper import (
    world_to_screen_x,
    world_to_screen_y
)


class Label:

    def __init__(self):

        # Position relative to aircraft, in WORLD coordinates
        self.offset_x = 20
        self.offset_y = 20

        # Interaction state
        self.dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        # Label dimensions
        self.width = 180
        self.line_height = 16

        self.buffer = 5

        # Data
        self.ssr_display = ""
        self.msg_special = ""
        self.msg_app = ""
        self.cs = ""
        self.next_sector = ""
        self.act_level = ""
        self.climb_descend_maintain = ""
        self.req_level = ""
        self.next_point = ""
        self.pfl = ""
        self.tfl = ""
        self.ecl = ""
        self.copx = ""
        self.gs = ""
        self.req_vertical_speed = ""
        self.act_vertical_speed = ""

        # Generated drawing data
        self.lines = []

        # Overall label rectangle in SCREEN coordinates
        self.rect = pygame.Rect(0, 0, 0, 0)

        # Individual field rectangles
        self.field_rects = []

    def get_world_position(self, aircraft):
        return (
            aircraft.pos_x + self.offset_x,
            aircraft.pos_y + self.offset_y
        )

    def build_label(self, aircraft):
        self.lines = [
            [
                str(aircraft.squawk),
                self.msg_special,
                self.msg_app
            ],
            [
                self.cs,
                self.next_sector,
            ],
            [
                str(aircraft.altitude_act),
                self.climb_descend_maintain,
                str(aircraft.altitude_req),
                self.next_point
            ],
            [
                self.pfl,
                self.tfl,
                self.ecl,
                self.copx,
            ],
            [
                str(aircraft.gs),
                str(aircraft.rate_of_climb_req),
                str(aircraft.rate_of_climb_act)
            ]
        ]

    def update_screen_rect(self, aircraft, camera):

        label_x, label_y = self.get_world_position(aircraft)

        screen_x = int(
            world_to_screen_x(
                label_x,
                camera.cam_offset_x,
                camera.zoom
            )
        )

        screen_y = int(
            world_to_screen_y(
                label_y,
                camera.cam_offset_y,
                camera.zoom
            )
        )

        self.rect = pygame.Rect(
            screen_x,
            screen_y,
            self.width,
            len(self.lines) * self.line_height
        )


    def mouse_down(self, mouse_pos, camera, aircraft):
        if not self.rect.collidepoint(mouse_pos):
            return False

        # Mouse -> world
        world_x = (
                          mouse_pos[0] + camera.cam_offset_x
                  ) / camera.zoom

        world_y = (
                      -(mouse_pos[1] + camera.cam_offset_y)
                  ) / camera.zoom

        label_x, label_y = self.get_world_position(aircraft)

        self.drag_offset_x = world_x - label_x
        self.drag_offset_y = world_y - label_y

        self.dragging = True

        return True

    def mouse_drag(self, mouse_pos, camera, aircraft):

        if not self.dragging:
            return

        world_x = (
                          mouse_pos[0] + camera.cam_offset_x
                  ) / camera.zoom

        world_y = (
                      -(mouse_pos[1] + camera.cam_offset_y)
                  ) / camera.zoom

        label_x = world_x - self.drag_offset_x
        label_y = world_y - self.drag_offset_y

        self.offset_x = label_x - aircraft.pos_x
        self.offset_y = label_y - aircraft.pos_y

    def mouse_up(self):
        self.dragging = False