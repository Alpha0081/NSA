import numpy as np
import numpy.typing as npt

from utils.basis import Axis, Basis, CartesianBasis
from utils.vector import Vector


class EccentricityValueError(Exception):
    def __str__(self) -> str:
        return "Eccentricity less than 0 or more or equal than 1"


class SemiMajorValueError(Exception):
    def __str__(self) -> str:
        return "Semi-major less or equal 0"


class Orbit:
    def __init__(
        self,
        eccentricity: float,
        inclination: float,
        raan: float,
        periapsis: float,
        semi_major: float,
    ):
        self.__validate(eccentricity, semi_major)

        self.__eccentricity: float = eccentricity
        self.__inclination: float = inclination
        self.__raan: float = raan
        self.__periapsis: float = periapsis
        self.__semi_major: float = semi_major
        self.__semi_minor: float = (1 - eccentricity ** 2) ** 0.5 * semi_major
        self.__get_basis()

    def __validate(
        self,
        eccentricity: float,
        semi_major: float,
    ) -> bool:
        self.__validate_eccentricity(eccentricity)
        self.__validate_semi_major(semi_major)
        return True

    def __validate_eccentricity(self, eccentricity: float) -> bool:
        if not 0 <= eccentricity < 1:
            raise EccentricityValueError
        return True

    def __validate_semi_major(self, semi_major: float) -> bool:
        if semi_major <= 0:
            raise SemiMajorValueError
        return True

    @property
    def basis(self) -> Basis:
        return self.__basis

    def __get_basis(self) -> bool:
        cartesian_basis: Basis = CartesianBasis()
        raan_rotate_basis: Basis = cartesian_basis.rotate(self.__raan)
        inclination_rotate_basis: Basis = raan_rotate_basis.rotate(
            -self.__inclination, Axis.OY
        )
        self.__basis = inclination_rotate_basis.rotate(self.__periapsis)
        return True

    def check(self, mean_anomaly, coords) -> bool:
        return (
            True if Vector(coords) == Vector(self.get_coords(mean_anomaly)) else False
        )

    def get_coords(self, mean_anomaly: float) -> npt.NDArray[np.float64]:
        current_E = mean_anomaly
        previous_E = 0.0
        eps = 1e-12

        while abs(current_E - previous_E) >= eps:
            previous_E = current_E
            current_E = mean_anomaly + self.__eccentricity * np.sin(current_E)

        x = np.cos(current_E) * self.__semi_major
        y = np.sin(current_E) * self.__semi_minor
        z = 0
        vector = np.array((x, y, z))
        return np.dot(self.__basis.matrix.transpose(), vector)

    def get_trace(self, size=50) -> npt.NDArray[np.float64]:
        basis = self.basis.matrix.transpose()
        phi = np.linspace(0, 2 * np.pi, size)
        x_axis = self.__semi_major * np.cos(phi)
        y_axis = self.__semi_minor * np.sin(phi)
        z_axis = np.zeros(size)
        matrix = np.array((x_axis, y_axis, z_axis))
        return np.dot(basis, matrix)
