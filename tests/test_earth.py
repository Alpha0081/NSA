from time import mktime, strptime

import numpy as np
import pytest
from earth import Earth, EarthParams
from utils.vector import Vector


@pytest.mark.parametrize(
    "longitude, latitude, coords",
    [
        (0, 0, np.array([EarthParams.semi_major, 0, 0])),
        (0, 90, np.array([0, 0, EarthParams.semi_minor])),
        (0, -90, np.array([0, 0, -EarthParams.semi_minor])),
        (180, 0, np.array([-EarthParams.semi_major, 0, 0])),
    ],
)
def test_get_object_coords(
    longitude: float, latitude: float, coords: np.ndarray
) -> None:
    test_time = mktime(strptime("1984-01-06T00:00:00", "%Y-%m-%dT%H:%M:%S"))
    earth = Earth(test_time)
    assert Vector(earth.get_object_coords(longitude, latitude)) == Vector(coords)
