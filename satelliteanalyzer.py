from time import time

from configloader import ConfigLoader
from satellitesystem import SatelliteSystem


class SatelliteAnalyzer:
    def __init__(self, root_path: str = "./"):
        config_loader = ConfigLoader(root_path)
        self.__satellite_systems: tuple[
            SatelliteSystem, ...
        ] = config_loader.get_satellite_systems_array()

    def synchronize(self, time_d: float = time() + 1) -> bool:
        for satellite_system in self.__satellite_systems:
            satellite_system.synchronize(time_d)
        return True

    @property
    def satellite_systems(self) -> tuple[SatelliteSystem, ...]:
        return self.__satellite_systems

    def move(self, time_step: float) -> bool:
        for satellite_system in self.__satellite_systems:
            satellite_system.move(time_step)
        return True


if __name__ == "__main__":
    SA = SatelliteAnalyzer()
    print(SA.satellite_systems[0].satellites_array[0].coords)
