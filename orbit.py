import numpy as np
import numpy.typing as npt

from utils.basis import Axis, Basis, CartesianBasis


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

    def get_current_coordinates(
        self, current_true_anomaly: float
    ) -> npt.NDArray[np.float64]:
        x = np.cos(current_true_anomaly) * self.__semi_major
        y_sign = 1 if np.sin(current_true_anomaly) >= 0 else 0
        y = (
            (-1) ** (y_sign + 1)
            * (1 - (x / self.__semi_major) ** 2) ** 0.5
            * self.__semi_minor
        )
        z = 0
        vector = np.array((x, y, z))
        return np.dot(self.__basis.matrix.transpose(), vector)

    def get_next_coordinate(self, mean_anomaly: float) -> npt.NDArray[np.float64]:
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
        return np.dot(self.__basis.matrix.transpose(), vector)

    def get_trace(self, size=50) -> npt.NDArray[np.float64]:
        x_axis: np.ndarray = np.zeros(size)
        y_axis: np.ndarray = np.zeros(size)
        z_axis: np.ndarray = np.zeros(size)
        basis: np.ndarray = self.basis.matrix.transpose()
        eccentricity: float = self.__eccentricity
        semi_major: float = self.__semi_major
        semi_minor: float = (1 - eccentricity ** 2) ** 0.5 * semi_major
        x_axis1: np.ndarray = np.linspace(-semi_major, semi_major, int(size // 2))
        y_axis1: np.ndarray = (1 - x_axis1 ** 2 / semi_major ** 2) ** 0.5 * semi_minor
        y_axis[: int(size // 2)] = y_axis1
        y_axis[int(size // 2) :] = -y_axis1
        x_axis[: int(size // 2)] = x_axis1
        x_axis[int(size // 2) :] = -x_axis1
        matrix: np.ndarray = np.array((x_axis, y_axis, z_axis))
        return np.dot(basis, matrix)
