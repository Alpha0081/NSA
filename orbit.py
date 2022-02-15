import numpy as np

from .utils.basis import Axis, Basis
from .utils.vector import Vector


class Orbit:
    def __init__(
        self,
        eccentricity: float,
        inclination: float,
        raan: float,
        periapsis: float,
        semi_major: float,
    ):
        self.__eccentricity = eccentricity
        self.__inclination = inclination
        self.__raan = raan
        self.__periapsis = periapsis
        self.__semi_major = semi_major
        self.__semi_minor = (1 - eccentricity ** 2) ** 0.5 * semi_major
        self.__basis = self.get_basis()

    def get_basis(self) -> Basis:
        cartesian_basis = Basis(
            Vector([1.0, 0.0, 0.0]), Vector([0.0, 1.0, 0.0]), Vector([0.0, 0.0, 1.0])
        )
        raan_rotate_basis = cartesian_basis.rotate(self.__raan)
        inclination_rotate_basis = raan_rotate_basis.rotate(self.__inclination, Axis.OX)
        return inclination_rotate_basis.rotate(self.__periapsis)

    def get_current_coordinate(self, current_true_anomaly: float) -> np.ndarray:
        x = np.cos(current_true_anomaly)
        y_sign = 1 if np.sin(current_true_anomaly) >= 0 else 0
        y = (
            (-1) ** (y_sign + 1)
            * (1 - (x / self.__semi_major) ** 2) ** 0.5
            * self.__semi_minor
        )
        z = 0
        vector = np.array((x, y, z))
        return np.dot(self.__basis.get_matrix().transpose(), vector)

    def get_next_coordinate(self, mean_anomaly: float) -> np.ndarray:
        current_E = 0
        previous_E = 1
        eps = 1e-12
        while abs(current_E - previous_E) >= eps:
            previous_E = current_E
            current_E = self.__eccentricity * np.sin(previous_E) + mean_anomaly
        x = np.cos(current_E) * self.__semi_major
        y = np.sin(current_E) * self.__semi_minor
        z = 0
        vector = np.array((x, y, z))
        return np.dot(self.__basis.get_matrix().transpose(), vector)

    def get_trace(self) -> np.ndarray:
        x_axis: np.ndarray = np.zeros(100)
        y_axis: np.ndarray = np.zeros(100)
        z_axis: np.ndarray = np.zeros(100)
        basis: np.ndarray = self.get_basis().get_matrix().transpose()
        eccentricity: float = self.__eccentricity
        semi_major: float = self.__semi_major
        semi_minor: float = (1 - eccentricity ** 2) ** 0.5 * semi_major
        x_axis1: np.ndarray = np.linspace(-semi_major, semi_major, 50)
        y_axis1: np.ndarray = (1 - x_axis1 ** 2 / semi_major ** 2) ** 0.5 * semi_minor
        y_axis[:50] = y_axis1
        y_axis[50:] = -y_axis1
        x_axis[:50] = x_axis1
        x_axis[50:] = -x_axis1
        matrix: np.ndarray = np.array((x_axis, y_axis, z_axis))
        return np.dot(basis, matrix)
