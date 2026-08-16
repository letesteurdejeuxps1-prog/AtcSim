import math

import pygame

from pages.radar.helpers.conversion_helper import (
    world_to_screen_x,
    world_to_screen_y
)


class Label:

    def __init__(self):

        # --------------------------------------------------------------
        # Position relative to aircraft, WORLD coordinates
        # --------------------------------------------------------------

        self.offset_x = 20
        self.offset_y = 20

        # --------------------------------------------------------------
        # Dragging
        # --------------------------------------------------------------

        self.dragging = False
        self.hovered_field = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        # --------------------------------------------------------------
        # Display
        # --------------------------------------------------------------

        self.line_height = 16
        self.buffer = 5
        self.field_padding_x = 3
        self.field_padding_y = 1
        self.field_hover_color = (70, 70, 120)

        # --------------------------------------------------------------
        # Data
        # --------------------------------------------------------------

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

        # --------------------------------------------------------------
        # Layout
        # --------------------------------------------------------------

        self.lines = []

        # {
        #     "field_name": pygame.Rect(...)
        # }
        self.field_rects = {}

        # Overall label rectangle
        self.rect = pygame.Rect(0, 0, 0, 0)

    # ==================================================================
    # POSITION
    # ==================================================================

    def get_world_position(self, aircraft):
        return (
            aircraft.pos_x + self.offset_x,
            aircraft.pos_y + self.offset_y
        )

    # ==================================================================
    # BUILD DATA
    # ==================================================================

    def build_label(self, aircraft):

        self.lines = [
            [
                ("ssr", str(aircraft.squawk)),
                ("msg_special", self.msg_special),
                ("msg_app", self.msg_app),
            ],
            [
                ("callsign", self.cs),
                ("next_sector", self.next_sector),
            ],
            [
                ("act_level", str(aircraft.altitude_act)),
                ("vertical_state", self.climb_descend_maintain),
                ("req_level", str(aircraft.altitude_req)),
                ("next_point", self.next_point),
            ],
            [
                ("pfl", self.pfl),
                ("tfl", self.tfl),
                ("ecl", self.ecl),
                ("copx", self.copx),
            ],
            [
                ("gs", str(aircraft.gs)),
                ("req_vertical_speed", str(aircraft.rate_of_climb_req)),
                ("act_vertical_speed", str(aircraft.rate_of_climb_act)),
            ]
        ]

    # ==================================================================
    # UPDATE LAYOUT
    # ==================================================================

    def update_layout(self, aircraft, camera, font):

        self.build_label(aircraft)

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

        self.field_rects.clear()

        current_y = screen_y
        max_right = screen_x

        for line in self.lines:

            current_x = screen_x

            for field_name, field_value in line:

                text_surface = font.render(
                    str(field_value),
                    True,
                    (255, 255, 255)
                )

                field_rect = pygame.Rect(
                    current_x - self.field_padding_x,
                    current_y - self.field_padding_y,
                    text_surface.get_width() + self.field_padding_x * 2,
                    self.line_height
                )

                self.field_rects[field_name] = field_rect

                current_x += (
                    text_surface.get_width()
                    + self.buffer
                )

                max_right = max(
                    max_right,
                    current_x
                )

            current_y += self.line_height

        self.rect = pygame.Rect(
            screen_x,
            screen_y,
            max_right - screen_x,
            len(self.lines) * self.line_height
        )

    # ==================================================================
    # FIELD HIT TEST
    # ==================================================================

    def get_field_at(self, mouse_pos):

        for field_name, rect in self.field_rects.items():

            if rect.collidepoint(mouse_pos):
                return field_name

        return None

    # ==================================================================
    # LABEL HIT TEST
    # ==================================================================

    def contains_point(self, mouse_pos):

        return self.rect.collidepoint(mouse_pos)

    # ==================================================================
    # DRAGGING
    # ==================================================================

    def mouse_down(self, mouse_pos, camera, aircraft):

        if not self.contains_point(mouse_pos):
            return False

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

    # ==================================================================
    # LEADER LINE
    # ==================================================================

    def get_connection_point(self, aircraft, camera):

        aircraft_x = world_to_screen_x(
            aircraft.pos_x,
            camera.cam_offset_x,
            camera.zoom
        )

        aircraft_y = world_to_screen_y(
            aircraft.pos_y,
            camera.cam_offset_y,
            camera.zoom
        )

        dx = aircraft_x - self.rect.centerx
        dy = aircraft_y - self.rect.centery

        angle = math.degrees(
            math.atan2(dy, dx)
        )

        angle %= 360

        direction = round(angle / 45) % 8

        points = {
            0: (self.rect.right, self.rect.centery),
            1: (self.rect.right, self.rect.bottom),
            2: (self.rect.centerx, self.rect.bottom),
            3: (self.rect.left, self.rect.bottom),
            4: (self.rect.left, self.rect.centery),
            5: (self.rect.left, self.rect.top),
            6: (self.rect.centerx, self.rect.top),
            7: (self.rect.right, self.rect.top),
        }

        return points[direction]

    def update_hover(self, mouse_pos):
        self.hovered_field = self.get_field_at(mouse_pos)