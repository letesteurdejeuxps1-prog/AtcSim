import json

from pages.radar.data.airspace_data.Area import Area
from pages.radar.data.airspace_data.Point import Point
from pages.radar.helpers.conversion_helper import convert_lat_and_long_to_radar, lat_long_to_local


class Airspace:

    def __init__(self):
        self.name = ""
        self.center = ""

        self.default_zoom = 1

        # Geographic origin of the simulation
        self.origin_lat = 0.0
        self.origin_lon = 0.0

        self.points = []
        self.areas = []
        self.aerodrome = []

    def load(self, airspace_file_path: str):

        with open(airspace_file_path, "r") as raw_data:
            data = json.load(raw_data)

        self.name = data["name"]
        self.center = data["center"]
        self.default_zoom = data["default_zoom"]

        # --------------------------------------------------
        # FIND ORIGIN
        # --------------------------------------------------

        origin_lon = None
        origin_lat = None

        for point_name, pt in data["points"].items():

            lon, lat = convert_lat_and_long_to_radar(
                pt["coord"]
            )

            if (
                str(point_name).upper()
                == str(self.center).upper()
                or
                str(pt.get("ABBR")).upper()
                == str(self.center).upper()
            ):
                origin_lon = lon
                origin_lat = lat
                break

        if origin_lon is None or origin_lat is None:
            raise ValueError(
                f"Could not find airspace center '{self.center}'"
            )

        self.origin_lon = origin_lon
        self.origin_lat = origin_lat

        # --------------------------------------------------
        # POINTS
        # --------------------------------------------------

        self.points = []

        for point_name, pt in data["points"].items():

            lon, lat = convert_lat_and_long_to_radar(
                pt["coord"]
            )

            x, y = lat_long_to_local(
                lat,
                lon,
                self.origin_lat,
                self.origin_lon
            )

            new_point = Point(
                point_name,
                pt.get("ABBR"),
                pt.get("TYPE"),
                x,
                y
            )

            self.points.append(new_point)

        # --------------------------------------------------
        # AREAS
        # --------------------------------------------------

        self.areas = []

        for area_name, area in data["areas"].items():

            coordinates = []

            for raw_coord in area["coord"]:

                lon, lat = convert_lat_and_long_to_radar(
                    raw_coord
                )

                x, y = lat_long_to_local(
                    lat,
                    lon,
                    self.origin_lat,
                    self.origin_lon
                )

                coordinates.append((x, y))

            new_area = Area(
                area["coord"],
                coordinates,
                area.get("limit_low"),
                area.get("limit_high"),
                area.get("highest_alt"),
                area.get("lowest_alt")
            )

            self.areas.append(new_area)