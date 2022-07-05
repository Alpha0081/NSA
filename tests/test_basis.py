import pytest
from utils.basis import Axis, Basis, CartesianBasis
from utils.vector import Vector


@pytest.mark.parametrize(
    "basis",
    [
        CartesianBasis(),
        Basis(Vector((1, 1e-12, 0)), Vector((0, 1, 0)), Vector((0, 0, 1))),
    ],
)
def test_basis_is_cartesian(basis: Basis) -> None:
    assert basis.is_cartesian


@pytest.mark.parametrize(
    "basis_input, basis_output, axis, angle",
    [
        (
            CartesianBasis(),
            Basis(Vector((0, 1, 0)), Vector((-1, 1e-12, 0)), Vector((0, 0, 1))),
            Axis.OZ,
            90,
        ),
        (
            CartesianBasis(),
            Basis(Vector((1, 0, 0)), Vector((0, 0, -1)), Vector((0, 1, 0))),
            Axis.OX,
            -90,
        ),
        (
            CartesianBasis(),
            Basis(Vector((-1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, -1))),
            Axis.OY,
            180,
        ),
    ],
)
def test_basis_rotation(
    basis_input: Basis, basis_output: Basis, axis: Axis, angle: float
) -> None:
    assert basis_input.rotate(angle, axis) == basis_output


@pytest.mark.xfail
def test_basis_rotation_error() -> None:
    basis: Basis = CartesianBasis()
    assert basis.rotate(0, "None")
