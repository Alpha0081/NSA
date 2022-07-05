from __future__ import annotations

from enum import Enum, auto

import numpy as np
import numpy.typing as npt

from utils.vector import Vector


class Axis(Enum):
    OX = auto()
    OY = auto()
    OZ = auto()


class AxisNameError(Exception):
    def __str__(self) -> str:
        return "Undefined axis name"


class Basis:
    def __init__(self, vector1: Vector, vector2: Vector, vector3: Vector) -> None:
        self._basis = np.array((vector1, vector2, vector3), dtype=Vector)

    def __repr__(self) -> str:
        return f"{tuple(map(lambda vector: str(vector), self._basis))}"

    def __eq__(self, other_basis: Basis) -> bool:
        is_equal = True
        for a, b in zip(self._basis, other_basis.basis):
            if a != b:
                is_equal = False
                break
        return is_equal

    @property
    def is_cartesian(self) -> bool:
        v1, v2, v3 = self._basis
        a = v1.is_orthogonal(v2)
        b = v2.is_orthogonal(v3)
        c = v3.is_orthogonal(v1)
        return all((a, b, c))

    @property
    def basis(self) -> np.ndarray:
        return self._basis

    @property
    def matrix(self) -> npt.NDArray[np.float64]:
        vector1, vector2, vector3 = self._basis
        return np.array(
            (vector1.coords, vector2.coords, vector3.coords),
            dtype=float,
        )

    def rotate(self, angle: float, axis_of_rotation: Axis = Axis.OZ) -> Basis:
        radian_angle = angle * np.pi / 180
        match axis_of_rotation:
            case Axis.OZ:
                x, y, z = self._basis[2].coords
            case Axis.OX:
                x, y, z = self._basis[0].coords
            case Axis.OY:
                x, y, z = self._basis[1].coords
            case _:
                raise AxisNameError

        rotation_matrix = [
            [
                np.cos(radian_angle) + (1 - np.cos(radian_angle)) * x ** 2,
                (1 - np.cos(radian_angle)) * x * y - np.sin(radian_angle) * z,
                (1 - np.cos(radian_angle)) * x * z + np.sin(radian_angle) * y,
            ],
            [
                (1 - np.cos(radian_angle)) * y * x + np.sin(radian_angle) * z,
                np.cos(radian_angle) + (1 - np.cos(radian_angle)) * y ** 2,
                (1 - np.cos(radian_angle)) * y * z - np.sin(radian_angle) * x,
            ],
            [
                (1 - np.cos(radian_angle)) * z * x - np.sin(radian_angle) * y,
                (1 - np.cos(radian_angle)) * z * y + np.sin(radian_angle) * x,
                np.cos(radian_angle) + (1 - np.cos(radian_angle)) * z ** 2,
            ],
        ]
        matrix = np.dot(rotation_matrix, self.matrix.transpose()).transpose()
        return Basis(Vector(matrix[0]), Vector(matrix[1]), Vector(matrix[2]))


class CartesianBasis(Basis):
    def __init__(self):
        self._basis = np.array(
            (Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1))), dtype=Vector
        )
