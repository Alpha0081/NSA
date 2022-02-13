import json

import numpy as np

from orbit import Orbit


class Satellite:
    def __init__(
        self,
        name: str,
        epoch: str,
        motion: float,
        eccentricity: float,
        inclination: float,
        raan: float,
        pericenter: float,
        anomaly: float,
        semi_major: int,
    ) -> None:
        self.name = name
        self.__epoch = epoch
        self.__motion = 2 * np.pi * motion / 86400
        self.__anomaly = anomaly * np.pi / 180
        self.__orbit = Orbit(eccentricity, inclination, raan, pericenter, semi_major)
        self.__set_start_coords()

    def draw(self):
        pass

    def get_height(self) -> float:
        out = 0
        for coord in self.__coords:
            out += coord ** 2
        return (out ** 0.5 - 6378137) / 1e3

    def __set_start_coords(self) -> None:
        self.__coords = self.__orbit.get_current_coordinate(self.__anomaly)

    def move(self, time: float = 1) -> None:
        self.__anomaly += time * self.__motion
        if self.__anomaly > np.pi:
            self.__anomaly -= 2 * np.pi
        elif self.__anomaly < -np.pi:
            self.__anomaly += 2 * np.pi
        self.__coords = self.__orbit.get_next_coordinate(self.__anomaly)

    def get_coords(self) -> np.ndarray:
        return self.__coords

    def get_epoch(self) -> str:
        return self.__epoch

    def get_trace(self):
        pass

    def disable_visible(self) -> None:
        self.__isVisible = False

    def enable_visible(self) -> None:
        self.__isVisible = True

    def get_visible(self) -> bool:
        return self.__isVisible

    def handler_visible_changed(self) -> None:
        self.__isVisible = not self.__isVisible

    __isVisible = True
    __coords = np.zeros(3)
