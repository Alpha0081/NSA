from __future__ import annotations
from typing import TypeVar
import numpy as np
import numpy.typing as npt


class VectorDimenstionError(Exception):
    def __str__(self):
        return f"Not 3D Vector"


T = TypeVar("T", int, float)


class Vector:
    def __init__(
        self,
        coords: npt.NDArray[np.int32 | np.float64] | list[T] | tuple[T, T, T],
    ) -> None:
        self.__coords: npt.NDArray[np.float64] = np.array(coords, dtype=float)
        if self.__coords.size != 3:
            raise VectorDimenstionError
        self.__coords /= self.length

    def __repr__(self) -> str:
        return f"{tuple(self.__coords)}"

    @property
    def length(self) -> float:
        sum: float = 0
        for coord in self.__coords:
            sum += coord ** 2
        return sum ** 0.5

    @property
    def coords(self) -> npt.NDArray[np.float64]:
        return self.__coords

    def get_dot_product(self, other_vector: Vector) -> float:
        out: float = 0
        for a, b in zip(self.__coords, other_vector.coords):
            out += a * b
        return out

    def is_orthogonal(self, other_vector: Vector, eps=1e-12) -> bool:
        return abs(self.get_dot_product(other_vector)) <= eps

    def __eq__(self, other_vector: object) -> bool:

        if not isinstance(other_vector, Vector):
            return NotImplemented

        summa: float = 0.0
        for a, b in zip(self.__coords, other_vector.coords):
            summa += (a - b) ** 2
        return True if summa ** 0.5 <= 1e-12 else False


if __name__ == "__main__":
    print(Vector([3, 34, 3]))
