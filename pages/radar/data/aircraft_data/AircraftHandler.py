from pages.radar.data.aircraft_data.Aircraft import Aircraft


class AircraftHandler:
    def __init__(self):
        self.aircraft_list: list[Aircraft] = []

    def update(self):
        pass

    def testing_populate_list(self, list_of_acft: list[Aircraft]):
        self.aircraft_list = list_of_acft