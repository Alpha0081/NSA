import time
from parser import Parser, ParserJSON

from net.almanacdownloader import AlmanacDownloader
from satellite import Satellite


class SatelliteSystem:
    def __init__(
        self,
        name_system: str,
        semi_major: int,
        almanac_url: str,
        root_path: str,
        current_time: float = time.time() + 1,
        update_almanac: bool = True,
    ):
        self.__name = name_system
        AlmanacDownloader(root_path, name_system, almanac_url, update_almanac)
        file_name = self.get_file_name(root_path)
        parser: Parser = ParserJSON(file_name)
        self.__satellite_array: tuple[Satellite, ...] = parser.parse(semi_major)
        self.synchronize(current_time)

    def synchronize(self, current_time: float) -> None:
        for satellite in self.__satellite_array:
            satellite_time = time.mktime(
                time.strptime(satellite.epoch, "%Y-%m-%dT%H:%M:%S.%f")
            )
            time_difference = current_time - satellite_time
            satellite.move(time_difference)

    @property
    def satellites_names_list(self) -> tuple[str, ...]:
        out = []
        for satellite in self.__satellite_array:
            out.append(satellite.name)
        return tuple(out)

    @property
    def name(self) -> str:
        return str(self.__name).split(".")[1]

    @property
    def satellites_array(self) -> tuple[Satellite, ...]:
        return self.__satellite_array

    def move(self, time_step: float) -> None:
        for satellite in self.__satellite_array:
            satellite.move(time_step)

    def get_file_name(self, root_path) -> str:
        return root_path + "data/" + self.__name.lower() + ".json"
