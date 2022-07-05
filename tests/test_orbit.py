import numpy as np
import numpy.typing as npt
import pytest
from orbit import Orbit
from utils.basis import Basis
from utils.vector import Vector


@pytest.mark.xfail
@pytest.mark.parametrize("eccentricity", [-1, 1])
def test_eccentricity_validation_error(eccentricity: float):
    assert Orbit(eccentricity, 0, 0, 0, 1)


@pytest.mark.xfail
def test_semi_major_validation_error():
    assert Orbit(0, 0, 0, 0, 0)


def test_orbit_basis():
    basis: Basis = Basis(
        Vector((0, 1 / 2 ** 0.5, 1 / 2 ** 0.5)),
        Vector((-1, 0, 0)),
        Vector((0, -1 / 2 ** 0.5, 1 / 2 ** 0.5)),
    )
    assert Orbit(0, 45, 90, 0, 3e7).basis == basis


@pytest.mark.parametrize(
    "mean_anomaly, coords",
    [
        (0, [-3e7, 0, 0]),
        (np.pi / 2, [0, -3e7 / 2 ** 0.5, -3e7 / 2 ** 0.5]),
        (np.pi, [1, 0, 0]),
        (3 * np.pi / 2, [0, 3e7 / 2 ** 0.5, 3e7 / 2 ** 0.5]),
    ],
)
def test_get_orbit_coords(mean_anomaly: float, coords: list[float]) -> None:
    orbit = Orbit(0, 45, 90, 90, 3e7)
    assert Vector(orbit.get_coords(mean_anomaly)) == Vector(coords)
