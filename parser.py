from abc import ABCMeta, abstractmethod
from satellite import Satellite
import json


class Parser:
    @abstractmethod
    def __init__(self, path: str) -> None:
        pass

    @abstractmethod
    def parse(self, semi_major: int) -> tuple[Satellite, ...]:
        pass


class ParserJSON(Parser):
    def __init__(self, path: str) -> None:
        self.__path = path

    def parse(self, semi_major: int) -> tuple[Satellite, ...]:
        satellites = []
        with open(self.__path, "r") as source_data:
            data = json.load(source_data)
            for satellite in data:
                satellites.append(
                    Satellite(
                        satellite["OBJECT_NAME"],
                        satellite["EPOCH"],
                        satellite["MEAN_MOTION"],
                        satellite["ECCENTRICITY"],
                        satellite["INCLINATION"],
                        satellite["RA_OF_ASC_NODE"],
                        satellite["ARG_OF_PERICENTER"],
                        satellite["MEAN_ANOMALY"],
                        semi_major,
                        satellite["NORAD_CAT_ID"],
                    )
                )
        return tuple(satellites)
