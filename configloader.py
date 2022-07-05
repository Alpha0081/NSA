import json
from os.path import isfile

from satellitesystem import SatelliteSystem


class ConfigLoader:
    def __init__(self, root_path: str) -> None:
        self.__root_path: str = root_path

    def __get_config_file_name(self) -> str:
        return (
            "config.json"
            if isfile(self.__root_path + "config/config.json")
            else "default.json"
        )

    def get_satellite_systems_array(self) -> tuple[SatelliteSystem, ...]:
        satellite_systems = []
        filename: str = self.__get_config_file_name()
        with open(self.__root_path + f"config/{filename}", "r") as f:
            config = json.load(f)
            for satellite_system in config["SATELLITE_SYSTEM"]:
                try:
                    enabled = satellite_system["ENABLED"]
                except KeyError:
                    enabled = True
                if enabled:
                    satellite_systems.append(
                        SatelliteSystem(
                            satellite_system["NAME"],
                            satellite_system["SEMI-MAJOR"],
                            satellite_system["URL"],
                            self.__root_path,
                        )
                    )
        return tuple(satellite_systems)


if __name__ == "__main__":
    c = ConfigLoader("./")
    a = c.get_satellite_systems_array()
    print(len(a))
