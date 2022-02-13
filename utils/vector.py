from __future__ import annotations
import numpy as np


class Vector:
    """
    Class for working with mathematical vectors
    """
    def __init__(self, coords: np.array) -> None:
        """
        Initialize
        """
        self.__coords: np.array = coords
        self.__normalize()

    def __repr__(self):
        return f"{tuple(self.__coords)}"

    def __normalize(self) -> None:
        self.__coords /= np.linalg.norm(self.__coords)
    
    def get_length(self) -> float:
        sum: float = 0
        for coord in self.__coords:
            sum += coord**2
        return sum ** .5

    def get_coords(self) -> np.array:
        return self.__coords

    def get_dot_product(self, other_vector: Vector) -> float:
        x, y, z = self.__coords
        i, j, k = other_vector.get_coords()
        return x * i + y * j + z * k
    
    def is_orthogonal(self, other_vector: Vector) -> bool:
        return self.get_dot_product(other_vector) == 0
