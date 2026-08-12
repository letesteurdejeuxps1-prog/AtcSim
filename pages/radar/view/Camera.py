from pages.radar.helpers.conversion_helper import world_to_screen_x


class Camera:

    def __init__(self):
        self.cam_offset_x = 0
        self.cam_offset_y = 0
        self.zoom = 10

    def set_center(self, screen_width, screen_height):
        self.cam_offset_x = -screen_width / 2
        self.cam_offset_y = -screen_height / 2

