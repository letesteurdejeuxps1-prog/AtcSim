import pygame


class Label:

    def __init__(self):
        self.buffer = 5
        self.lines: list = []


        self.ssr_display = ""
        self.ssr_display_rect = pygame.rect.Rect(0, 0, 0, 0)

        self.msg_special = ""
        self.msg_special_rect = pygame.rect.Rect(0, 0, 0, 0)

        self.msg_app = ""
        self.msg_app_rect = pygame.rect.Rect(0, 0, 0, 0)

        self.cs = ""
        self.cs_rect = pygame.rect.Rect(0, 0, 0, 0)

        self.next_sector = ""
        self.next_sector_rect = pygame.rect.Rect(0, 0, 0, 0)

        self.act_level = ""
        self.act_level_rect = pygame.rect.Rect(0, 0, 0, 0)

        self.climb_descend_maintain = ""
        self.climb_descend_maintain_rect = pygame.rect.Rect(0, 0, 0, 0)

        self.req_level = ""
        self.req_level_rect = pygame.rect.Rect(0, 0, 0, 0)

        self.next_point = ""
        self.next_point_rect = pygame.rect.Rect(0, 0, 0, 0)

        self.pfl = ""
        self.pfl_rect = pygame.rect.Rect(0, 0, 0, 0)

        self.tfl = ""
        self.tfl_rect = pygame.rect.Rect(0, 0, 0, 0)

        self.ecl = ""
        self.ecl_rect = pygame.rect.Rect(0, 0, 0, 0)

        self.copx = ""
        self.copx_rect = pygame.rect.Rect(0, 0, 0, 0)

        self.gs = ""
        self.gs_rect = pygame.rect.Rect(0, 0, 0, 0)

        self.req_vertical_speed = ""
        self.req_vertical_speed_rect = pygame.rect.Rect(0, 0, 0, 0)

        self.act_vertical_speed = ""
        self.act_vertical_speed_rect = pygame.rect.Rect(0, 0, 0, 0)

    def build_label(self):
        self.lines.append([
            self.ssr_display,
            self.msg_special,
            self.msg_app
        ])
        self.lines.append([
            self.cs,
            self.next_sector,
        ])
        self.lines.append([
            self.act_level,
            self.climb_descend_maintain,
            self.req_level,
            self.next_point
        ])
        self.lines.append([
            self.pfl,
            self.tfl,
            self.ecl,
            self.copx,
        ])
        self.lines.append([
            self.gs,
            self.req_vertical_speed,
            self.act_vertical_speed
        ])
