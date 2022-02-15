from time import mktime, strptime

import numpy as np
from .utils.basis import Basis
from .utils.vector import Vector

class Earth:
    def __init__(self, current_time: float):
        epoch_start = mktime(strptime("06.01.1984T00:00:00", "%d.%m.%YT%H:%M:%S"))
        self.move(current_time - epoch_start)

    def get_emitter_coords(self, longitude: float, latitude: float) -> np.ndarray:
        phi = longitude * np.pi / 180
        theta = latitude * np.pi / 180
        x = self.__semi_major * np.cos(phi) * np.cos(theta)
        y = self.__semi_major * np.sin(phi) * np.cos(theta)
        z = self.__semi_minor * np.sin(theta)
        vector = np.array((x, y, z))
        return np.dot(self.__basis.get_matrix().transpose(), vector)

    def move(self, time: float = 1):
        self.__basis.rotate(self.__radian_motion * 180 / np.pi * time)

    __semi_major = 6378137
    __radian_motion = 7292115e-11
    __flattering = 1 / 298.257223563
    __semi_minor = __semi_major * (1 - __flattering)
    __basis = Basis(Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 0, 1]))
