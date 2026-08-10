class Area:
    def __init__(
            self,
            coordinates: list[str],
            coordinates_converted: list,
            limit_low: int,
            limit_high: int,
            highest_alt: int,
            lowest_alt: int
    ):
        self.coordinates_raw = coordinates
        self.coordinates_converted = coordinates_converted
        self.limit_low = int(limit_low)
        self.limit_high = int(limit_high)
        self.highest_alt = int(highest_alt)
        self.lowest_alt = int(lowest_alt)

