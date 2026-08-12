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

        self.rate_of_turn_req = 3
        self.rate_of_turn_act = 3

        self.rate_of_climb_req = 0
        self.rate_of_climb_act = 0

        self.acceleration_gradient = 0

        self.color_body = (255, 255, 255)
        self.color_history_dots = (255, 255, 255)
        self.color_prl = (255, 255, 255)

        self.route = ""

