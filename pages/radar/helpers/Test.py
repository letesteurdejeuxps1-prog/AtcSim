import json

from pages.radar.data.aircraft_data.Aircraft import Aircraft
from pages.radar.helpers.conversion_helper import convert_lat_and_long_to_radar, lat_long_to_local


class Test:

    def __init__(self):
        pass

    def load_acft(self, root_directory, origin_lon, origin_lat):
        return_data = []
        file = "{}\\pages\\radar\\debug\\acft.json".format(root_directory)
        with open(file, 'r') as raw_data:
            data = json.load(raw_data)
            for acft in data["acft"]:
                new_acft = Aircraft()
                lon, lat = convert_lat_and_long_to_radar(
                    f"{acft['coord_x']}|{acft['coord_y']}"
                )

                x, y = lat_long_to_local(
                    lat,
                    lon,
                    origin_lat,
                    origin_lon
                )
                new_acft.pos_x = x
                new_acft.pos_y = y
                new_acft.type = acft['type']
                new_acft.squawk = str(acft['ssr'])
                new_acft.wtc = 'M'
                new_acft.ias_req = acft['req_speed_kts']
                new_acft.ias_act = acft['act_speed_kts']
                new_acft.heading_req = acft['heading_req']
                new_acft.heading_act = acft['heading_act']
                new_acft.altitude_req = acft['altitude_req']
                new_acft.altitude_act = acft['altitude_act']
                new_acft.route = acft['route']
                return_data.append(new_acft)
        return return_data