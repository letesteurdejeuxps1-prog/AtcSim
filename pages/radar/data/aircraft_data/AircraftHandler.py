from pages.radar.data.aircraft_data.Aircraft import Aircraft


class AircraftHandler:
    def __init__(self):
        self.mode_a: bool = True
        self.mode_s: bool = True
        self.mode_v: bool = True
        self.aircraft_list: list[Aircraft] = []

    def update(self, radar_elapsed_time):
        if radar_elapsed_time is None:
            return

        for aircraft in self.aircraft_list:
            aircraft.update_acft(radar_elapsed_time)

    def set_prl_length(self, duration_in_sec: int):
        for aircraft in self.aircraft_list:
            aircraft.prl_length_in_sec = duration_in_sec
            aircraft.prl_end_x, aircraft.prl_end_y = aircraft.update_prl_data()

    def mode_to_switch(self, mode_to_switch):
        if mode_to_switch == 'A':
            self.mode_a = not self.mode_a
        if mode_to_switch == 'S':
            self.mode_s = not self.mode_s
        if mode_to_switch == 'V':
            self.mode_v = not self.mode_v

    def get_label_info(self):
        return self.mode_a, self.mode_s, self.mode_v

    def testing_populate_list(self, list_of_acft: list[Aircraft]):
        self.aircraft_list = list_of_acft