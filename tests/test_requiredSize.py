"""
Copyright (c) 2024 Anthony Tropeano
All Rights Reserved.
"""

import pytest
from NG_Subnet.NG_Subnet_Calculator import calculateRequiredSubnetSize


def test_calculateRequiredSubnetSize():
    # Testing with the correct expected subnet sizes (in CIDR notation)
    assert calculateRequiredSubnetSize(10) == 28  # /28 (16 total, 14 usable)
    assert calculateRequiredSubnetSize(100) == 25  # /25 (128 total, 126 usable)
    assert calculateRequiredSubnetSize(1000) == 22  # /22 (1024 total, 1022 usable)
    assert calculateRequiredSubnetSize(10000) == 18  # /18 (16384 total, 16382 usable)
    assert (
        calculateRequiredSubnetSize(100000) == 15
    )  # /15 (131072 total, 131070 usable)
    assert (
        calculateRequiredSubnetSize(1000000) == 12
    )  # /13 (524288 total, 524286 usable)
    assert (
        calculateRequiredSubnetSize(10000000) == 8
    )  # /10 (4194304 total, 4194302 usable)
    assert (
        calculateRequiredSubnetSize(100000000) == 5
    )  # /8 (16777216 total, 16777214 usable)
    assert (
        calculateRequiredSubnetSize(1000000000) == 2
    )  # /4 (1073741824 total, 1073741822 usable)

    # Ensure the function raises a ValueError for too many hosts
    with pytest.raises(ValueError):
        calculateRequiredSubnetSize(10000000000)
