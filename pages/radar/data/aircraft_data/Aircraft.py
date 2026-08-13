from pages.radar.helpers.math_helper import get_cos_angle, get_rad_angle, get_sin_angle


class Aircraft:

    # Display values
    body_width = 10
    body_height = 10
    history_dots_radius = 2

    # LNAV modes
    NAV_HEADING: int = 0
    NAV_ROUTE: int = 1

    def __init__(self):

        # Display values
        self.pos_x = 0
        self.pos_y = 0

        # Fixed values
        self.type = ""
        self.wtc = ""
        self.squawk = ""

        # Changeable values
        self.heading_req = 0
        self.heading_act = 0

        self.altitude_req = 0
        self.altitude_act = 0

        self.ias_req = 0
        self.ias_act = 0
        self.gs = 0

        self.rate_of_turn_req = 3
        self.rate_of_turn_act = 3

        self.rate_of_climb_req = 0
        self.rate_of_climb_act = 0

        self.acceleration_gradient = 0

        self.color_body = (255, 255, 255)
        self.color_history_dots = (255, 255, 255)
        self.color_prl = (255, 255, 255)

        self.route = ""

    def update_acft(self, elapsed_time_ms: int):
        elapsed_time = elapsed_time_ms / 1000
        self.update_speed()
        self.update_level()
        self.update_heading()
        self.move(elapsed_time)

    def update_speed(self):
        # TODO Calc GS
        self.gs = self.ias_act

    def update_level(self):
        pass

    def update_heading(self):
        pass

    def move(self, elapsed_time: int | float):
        next_x, next_y = self.next_pos(
            get_rad_angle(self.heading_act),
            elapsed_time
        )
        self.pos_x = next_x
        self.pos_y = next_y

    def next_pos(self, r_angle, amount_of_sec):

        next_x = (
            self.pos_x
            + get_cos_angle(r_angle)
            * self.get_gs_speed_per_sec()
            * amount_of_sec
        )

        next_y = (
            self.pos_y
            + get_sin_angle(r_angle)
            * self.get_gs_speed_per_sec()
            * amount_of_sec
        )

        return next_x, next_y

    def get_gs_speed_per_sec(self) -> float:
        return self.gs / 3600