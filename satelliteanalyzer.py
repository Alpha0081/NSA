import json
from os.path import isfile
from time import time, sleep

import numpy as np

from .satellitesystem import SatelliteSystem


class SatelliteAnalyzer:
    def __init__(self, root_path: str):
        self.load_config(root_path)

    # @todo Добавить загрузку различных форматов файлов альманахов
    def load_config(self, root_path: str) -> None:
        if isfile(root_path + "config/config.json"):
            pass
        elif isfile(root_path + "config/default.json"):
            with open(root_path + "config/default.json", "r") as raw:
                config = json.load(raw)
                self.__satellite_systems = np.zeros(
                    len(config["SATELLITE_SYSTEM"]), dtype=SatelliteSystem
                )
                for i, satellite_system in enumerate(config["SATELLITE_SYSTEM"]):
                    print(satellite_system)
                    self.__satellite_systems[i] = SatelliteSystem(
                        satellite_system["NAME"],
                        satellite_system["SEMI-MAJOR"],
                        satellite_system["URL"],
                        root_path,
                    )
            raw.close()

    # @todo Добавить во входной параметр время синхронизации
    def synchronize(self, current_time=time() + 1) -> None:
        for satellite_system in self.__satellite_systems:
            satellite_system.synchronize(current_time)

    def move(self) -> None:
        for satellite_system in self.__satellite_systems:
            satellite_system.move()

if __name__ == "__main__":
    SA = SatelliteAnalyzer("./")
    SA.synchronize()
