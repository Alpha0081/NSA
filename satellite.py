import numpy as np
import numpy.typing as npt

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
        norad: int,
    ) -> None:
        self.__coords: npt.NDArray[np.float64] = np.zeros(3, dtype=float)
        self.__name: str = name
        self.__epoch: str = epoch
        self.__motion: float = 2 * np.pi * motion / 86400
        self.__anomaly: float = anomaly * np.pi / 180
        self.__orbit: Orbit = Orbit(
            eccentricity, inclination, raan, pericenter, semi_major
        )
        self.__coords: npt.NDArray[np.float64] = self.__orbit.get_coords(self.__anomaly)
        self.__norad: int = norad

    def move(self, time: float = 1) -> None:
        self.__anomaly += time * self.__motion
        if self.__anomaly > np.pi:
            self.__anomaly -= 2 * np.pi
        elif self.__anomaly < -np.pi:
            self.__anomaly += 2 * np.pi
        self.__coords = self.__orbit.get_coords(self.__anomaly)

    @property
    def norad(self) -> str:
        return str(self.__norad)

    @property
    def coords(self) -> npt.NDArray[np.float64]:
        return self.__coords

    @property
    def epoch(self) -> str:
        return self.__epoch

    def get_trace(self, size: int = 50) -> np.ndarray:
        return self.__orbit.get_trace(size)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def anomaly(self) -> float:
        return self.__anomaly
