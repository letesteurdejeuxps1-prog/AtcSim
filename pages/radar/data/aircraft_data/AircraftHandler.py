from pages.radar.data.aircraft_data.Aircraft import Aircraft


class AircraftHandler:
    def __init__(self):
        self.aircraft_list: list[Aircraft] = []

    def update(self, elapsed_time: int):
        for aicraft in self.aircraft_list:
            aicraft.update_acft(elapsed_time)

    def testing_populate_list(self, list_of_acft: list[Aircraft]):
        self.aircraft_list = list_of_acft