import numpy as np
from utils.vector import Vector
from enum import Enum, auto


class Axis(Enum):
    OX = auto()
    OY = auto()
    OZ = auto()
    

class Basis:
    def __init__(self, 
            vector1: Vector, 
            vector2: Vector, 
            vector3: Vector) -> None:
        self.__basis = np.array((vector1, vector2, vector3), dtype=Vector)

    def __repr__(self):
        return f"{tuple(map(lambda vector: str(vector), self.__basis))}"

    def orthogonality_check(self, 
            vector1: Vector, 
            vector2: Vector, 
            vector3: Vector) -> bool:
        a = vector1.is_orthogonal(vector2)
        b = vector2.is_orthogonal(vector3)
        c = vector3.is_orthogonal(vector1)
        if not all((a, b, c)):
            raise ValueError(f"vectors in basis is not orthogonality")
        return True

    def get_matrix(self) -> np.array:
        vector1, vector2, vector3 = self.__basis
        return np.array((vector1.get_coords(), 
            vector2.get_coords(), 
            vector3.get_coords()), dtype=float)

    def draw(self, ax, color=None) -> None:
        for vector in self.__basis:
            vector.draw(ax, color)

    def rotate(self, angle: float, axis_of_rotation=Axis.OZ):
        radian_angle = angle * np.pi / 180
        if axis_of_rotation == Axis.OZ:
            x, y, z = self.__basis[2].get_coords()
        elif axis_of_rotation == Axis.OX:
            x, y, z = self.__basis[0].get_coords()
        elif axis_of_rotation == Axis.OY:
            x, y, z = self.__basis[1].get_coords()
        else:
            raise ValueError("nonexistent axis")

        rotation_matrix = [[np.cos(radian_angle) + (1 - np.cos(radian_angle)) * x ** 2,
                            (1 - np.cos(radian_angle)) * x * y - np.sin(radian_angle) * z,
                            (1 - np.cos(radian_angle)) * x * z + np.sin(radian_angle) * y],
                            [(1 - np.cos(radian_angle)) * y * x + np.sin(radian_angle) * z,
                            np.cos(radian_angle) + (1 - np.cos(radian_angle)) * y ** 2,
                            (1 - np.cos(radian_angle)) * y * z - np.sin(radian_angle) * x],
                            [(1 - np.cos(radian_angle)) * z * x - np.sin(radian_angle) * y,
                            (1 - np.cos(radian_angle)) * z * y + np.sin(radian_angle) * x,
                            np.cos(radian_angle) + (1 - np.cos(radian_angle)) * z ** 2]]
        matrix = np.dot(rotation_matrix, self.get_matrix().transpose()).transpose()
        return Basis(Vector(matrix[0]), Vector(matrix[1]), Vector(matrix[2]))
