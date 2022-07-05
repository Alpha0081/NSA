import pytest
from satellite import Satellite
from numpy import pi
from utils.vector import Vector


@pytest.mark.parametrize("time_move", [1, 60, 3600, 86400, 100000])
def test_satellite_anomaly(time_move) -> None:
    satellite = Satellite("Test", "2022-06-19T00:00:00", 1, 0, 0, 0, 0, 0, 1, 0)
    satellite.move(time_move)
    assert -pi <= satellite.anomaly <= pi


@pytest.mark.parametrize(
    "motion, time_move",
    [(1, 86400), (1, 2 * 86400), (1.2, 86400 / 1.2), (1.4, 2 * 86400 / 1.4)],
)
def test_satellite_move(motion: float, time_move: float) -> None:
    satellite = Satellite("Test", "2022-06-19T00:00:00", motion, 0, 0, 0, 0, 0, 1, 0)
    coords = satellite.coords
    satellite.move(time_move)
    assert Vector(satellite.coords) == Vector(coords)
