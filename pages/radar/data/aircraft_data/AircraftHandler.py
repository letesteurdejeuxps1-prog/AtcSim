from pages.radar.data.aircraft_data.Aircraft import Aircraft


class AircraftHandler:
    def __init__(self):
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

    def testing_populate_list(self, list_of_acft: list[Aircraft]):
        self.aircraft_list = list_of_acft