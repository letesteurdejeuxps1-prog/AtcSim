from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from pages.radar.Main import Main


class EventHandler:

    def __init__(self, parent: "Main"):
        self.parent = parent

        # Object currently being interacted with
        self.dragging_label = None
        self.dragging_aircraft = None
        self.dragging_window = None

    def handle_event(self, event: pygame.event.Event):

        # Quit
        if (
            event.type == pygame.QUIT
            or (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_q
            )
        ):
            self.parent.is_running = False

        # Mouse wheel
        elif event.type == pygame.MOUSEWHEEL:
            self.handle_event_scroll(event)

        # Mouse button down
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_event_mouseclick(event)

        # Mouse button up
        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_event_mouseclick_off(event)

        # Mouse movement
        elif event.type == pygame.MOUSEMOTION:
            self.handle_mouse_motion(event)

    # ------------------------------------------------------------------
    # Mouse wheel
    # ------------------------------------------------------------------

    def handle_event_scroll(self, event: pygame.event.Event):

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Convert mouse position to world coordinates
        world_x = (
            mouse_x + self.parent.camera.cam_offset_x
        ) / self.parent.camera.zoom

        world_y = (
            -(mouse_y + self.parent.camera.cam_offset_y)
        ) / self.parent.camera.zoom

        zoom_factor = 1.1 if event.y > 0 else 0.9

        self.parent.camera.zoom *= zoom_factor

        self.parent.camera.zoom = max(
            0.1,
            min(self.parent.camera.zoom, 500)
        )

        # Keep the point under the mouse stationary
        self.parent.camera.cam_offset_x = (
            world_x * self.parent.camera.zoom - mouse_x
        )

        self.parent.camera.cam_offset_y = (
            -world_y * self.parent.camera.zoom - mouse_y
        )

    # ------------------------------------------------------------------
    # Mouse button down
    # ------------------------------------------------------------------

    def handle_event_mouseclick(self, event: pygame.event.Event):

        mouse_pos = event.pos

        if event.button == 1:

            self.parent.left_click_on = True

            # --------------------------------------------------------------
            # Windows have highest priority
            # --------------------------------------------------------------

            for window in reversed(self.parent.screen.window_list):

                if not window.visible:
                    continue

                if window.mouse_down(mouse_pos):
                    self.dragging_window = window

                    # Put clicked window on top
                    self.parent.screen.window_list.remove(window)
                    self.parent.screen.window_list.append(window)

                    return

            # --------------------------------------------------------------
            # Aircraft labels
            # --------------------------------------------------------------

            for aircraft in self.parent.aircraft_handler.aircraft_list:

                label = aircraft.label

                field = label.get_field_at(mouse_pos)

                if field is not None:
                    self.handle_label_field_click(
                        aircraft,
                        field
                    )
                    return

                if label.mouse_down(
                        mouse_pos,
                        self.parent.camera,
                        aircraft
                ):
                    self.dragging_label = label
                    self.dragging_aircraft = aircraft
                    return

            # --------------------------------------------------------------
            # Main menu
            # --------------------------------------------------------------

            self.parent.screen.main_menu.mouse_down(mouse_pos)

        elif event.button == 2:
            self.parent.middle_click_on = True

        elif event.button == 3:
            self.parent.right_click_on = True

    # ------------------------------------------------------------------
    # Mouse button up
    # ------------------------------------------------------------------

    def handle_event_mouseclick_off(self, event):

        mouse_pos = event.pos

        if event.button == 1:

            self.parent.left_click_on = False

            if self.dragging_window is not None:

                self.dragging_window.mouse_up(mouse_pos)

                self.dragging_window = None

            elif self.dragging_label is not None:

                self.dragging_label.mouse_up()

                self.dragging_label = None
                self.dragging_aircraft = None

            self.parent.screen.main_menu.mouse_up(mouse_pos)

        elif event.button == 2:
            self.parent.middle_click_on = False

        elif event.button == 3:
            self.parent.right_click_on = False


    # ------------------------------------------------------------------
    # Mouse movement
    # ------------------------------------------------------------------

    def handle_mouse_motion(self, event):

        mouse_pos = event.pos

        # Menu hover
        self.parent.screen.main_menu.update_mouse(mouse_pos)

        # Aircraft label hover
        for aircraft in self.parent.aircraft_handler.aircraft_list:
            aircraft.label.update_hover(mouse_pos)

        # Label dragging
        if (
                self.dragging_label is not None
                and self.dragging_aircraft is not None
        ):
            self.dragging_label.mouse_drag(
                mouse_pos,
                self.parent.camera,
                self.dragging_aircraft
            )

        # Camera panning
        if (
                self.parent.middle_click_on
                or self.parent.right_click_on
        ):
            self.handle_event_mouse_middle_click_drag(event)


    def handle_event_mouse_middle_click_drag(
            self,
            event: pygame.event.Event
    ):

        if isinstance(event.rel, tuple) and len(event.rel) == 2:

            self.parent.camera.cam_offset_x -= event.rel[0]
            self.parent.camera.cam_offset_y -= event.rel[1]

    def handle_label_field_click(
            self,
            aircraft,
            field_name: str
    ):
        if field_name == "act_level":
            print("# Open altitude window of acft {}".format(aircraft.squawk))
            pass

        elif field_name == "req_level":
            print("# Open requested altitude window of acft {}".format(aircraft.squawk))
            pass

        elif field_name == "ssr":
            print("# Open squawk window of acft {}".format(aircraft.squawk))
            pass

        elif field_name == "callsign":
            print("# Open callsign/aircraft information window of acft {}".format(aircraft.squawk))
            pass