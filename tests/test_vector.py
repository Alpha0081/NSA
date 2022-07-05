import numpy as np
import numpy.typing as npt
import pytest
from utils.vector import Vector
from typing import TypeVar

T = TypeVar("T", int, float)


@pytest.mark.parametrize(
    "array", [(1.0, 2.0, 4.0), [1.0, 2.0, 3.0], np.array([1, 2, 0])]
)
def test_vector_init(
    array: list[T] | tuple[T, T, T] | npt.NDArray[np.float64 | np.int32]
) -> None:
    a = Vector(array)
    assert type(a) == Vector


@pytest.mark.xfail
def test_vector_error_dimension():
    assert Vector([1, 2])


@pytest.mark.parametrize(
    "vector",
    [Vector([3, 4, 4]), Vector([4, 5, 4]), Vector([np.pi, np.exp(1), np.log(2)])],
)
def test_vector_length(vector: Vector, eps=1e-12) -> None:
    assert vector.length == 1


@pytest.mark.parametrize(
    "a, b",
    [(Vector([2, -2, 0]), Vector((2, 2, 0)))],
)
def test_vector_orthogonal(a: Vector, b: Vector) -> None:
    assert a.is_orthogonal(b)


@pytest.mark.parametrize("a, b", [(Vector([1, 0, 0]), Vector((1, 1e-12, 0)))])
def test_vector_equals(a: Vector, b: Vector) -> None:
    assert a == b


@pytest.mark.xfail
def test_vector_not_equals() -> None:
    assert Vector((1, 0, 0)) == Vector((1, 1e-12, 1e-12))
