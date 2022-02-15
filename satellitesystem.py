import json
import time

import numpy as np

from .satellite import Satellite
from .net.almanacdownloader import AlmanacDownloader 

class SatelliteSystem:
    def __init__(self, name_system: str, semi_major: float, almanac_url: str, root_path: str, current_time: float = time.time() + 1):
        self.__name = name_system
        AlmanacDownloader(root_path, name_system, almanac_url)        
        self.__satellite_nums = self.get_satellite_nums(root_path)
        self.__satellite_array = np.zeros(self.__satellite_nums, dtype=Satellite)
        file_name = self.get_file_name(root_path)
        with open(file_name, "r") as raw_data:
            src = json.load(raw_data)
            for i, satellite in enumerate(src):
                name = satellite["OBJECT_NAME"]
                epoch = satellite["EPOCH"]
                motion = satellite["MEAN_MOTION"]
                eccentricity = satellite["ECCENTRICITY"]
                inclination = satellite["INCLINATION"]
                raan = satellite["RA_OF_ASC_NODE"]
                pericenter = satellite["ARG_OF_PERICENTER"]
                anomaly = satellite["MEAN_ANOMALY"]
                self.__satellite_array[i] = Satellite(
                    name,
                    epoch,
                    motion,
                    eccentricity,
                    inclination,
                    raan,
                    pericenter,
                    anomaly,
                    semi_major,
                )
        raw_data.close()
        self.synchronize(current_time)

    def get_satellite_nums(self, root_path) -> int:
        file_name = self.get_file_name(root_path)
        with open(file_name, "r") as raw_data:
            num = len(json.load(raw_data))
        raw_data.close()
        return num

    def synchronize(self, current_time: float) -> None:
        for satellite in self.__satellite_array:
            satellite_time = time.mktime(
                time.strptime(satellite.get_epoch(), "%Y-%m-%dT%H:%M:%S.%f")
            )
            time_difference = current_time - satellite_time
            satellite.move(time_difference)

    def get_satellites_names_list(self) -> np.ndarray:
        out = []
        for satellite in self.__satellite_array:
            out.append(satellite.name)
        return np.array(out)

    def get_navigation_system_name(self) -> str:
        return str(self.__name).split(".")[1]

    def disable_visible(self) -> None:
        self.__isVisible = False

    def get_satellites_array(self) -> np.ndarray:
        return self.__satellite_array

    def enable_visible(self) -> None:
        self.__isVisible = True

    def get_visible(self) -> bool:
        return self.__isVisible

    def move(self) -> None:
        for satellite in self.__satellite_array:
            satellite.move()

    def get_file_name(self, root_path) -> str:
        return root_path + "data/" + self.__name.lower() + ".json"

    __isVisible = True
