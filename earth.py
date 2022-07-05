from dataclasses import dataclass
from time import mktime, strptime

import numpy as np

from utils.basis import Basis, CartesianBasis


@dataclass
class EarthParams:
    semi_major: float = 6378137
    radian_motion: float = 7292115e-11
    flattering: float = 1 / 298.257223563
    semi_minor: float = semi_major * (1 - flattering)


class Earth:
    def __init__(self, current_time: float):
        epoch_start = mktime(strptime("06.01.1984T00:00:00", "%d.%m.%YT%H:%M:%S"))
        self.__basis = CartesianBasis()
        self.move(current_time - epoch_start)

    def get_object_coords(self, longitude: float, latitude: float) -> np.ndarray:
        phi = longitude * np.pi / 180
        theta = latitude * np.pi / 180
        x = EarthParams.semi_major * np.cos(phi) * np.cos(theta)
        y = EarthParams.semi_major * np.sin(phi) * np.cos(theta)
        z = EarthParams.semi_minor * np.sin(theta)
        vector = np.array((x, y, z))
        return np.dot(self.__basis.matrix, vector)

    def move(self, time: float = 1):
        self.__basis.rotate(EarthParams.radian_motion * 180 / np.pi * time)

    @property
    def basis(self) -> Basis:
        return self.__basis
