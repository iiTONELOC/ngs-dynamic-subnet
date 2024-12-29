"""
Copyright (c) 2024 Anthony Tropeano
All Rights Reserved.
"""

import pytest
from NG_Subnet import generateDynamicSubnets

expectedData = {
    "Subnet-1": {
        "subnet": "10.0.0.0/26",
        "usable_range": "10.0.0.1 - 10.0.0.62",
        "netmask": "255.255.255.192",
        "broadcast": "10.0.0.63",
        "gateway": "10.0.0.1",
        "dhcp_range_start": "10.0.0.10",
        "dhcp_range_end": "10.0.0.62",
        "dns": ["1.1.1.1", "1.0.0.1"],
    },
    "Subnet-2": {
        "subnet": "10.0.0.64/26",
        "usable_range": "10.0.0.65 - 10.0.0.126",
        "netmask": "255.255.255.192",
        "broadcast": "10.0.0.127",
        "gateway": "10.0.0.65",
        "dhcp_range_start": "10.0.0.74",
        "dhcp_range_end": "10.0.0.126",
        "dns": ["1.1.1.1", "1.0.0.1"],
    },
    "Subnet-3": {
        "subnet": "10.0.0.128/26",
        "usable_range": "10.0.0.129 - 10.0.0.190",
        "netmask": "255.255.255.192",
        "broadcast": "10.0.0.191",
        "gateway": "10.0.0.129",
        "dhcp_range_start": "10.0.0.138",
        "dhcp_range_end": "10.0.0.190",
        "dns": ["1.1.1.1", "1.0.0.1"],
    },
    "Subnet-4": {
        "subnet": "10.0.0.192/26",
        "usable_range": "10.0.0.193 - 10.0.0.254",
        "netmask": "255.255.255.192",
        "broadcast": "10.0.0.255",
        "gateway": "10.0.0.193",
        "dhcp_range_start": "10.0.0.202",
        "dhcp_range_end": "10.0.0.254",
        "dns": ["1.1.1.1", "1.0.0.1"],
    },
    "Subnet-5": {
        "subnet": "10.0.1.0/26",
        "usable_range": "10.0.1.1 - 10.0.1.62",
        "netmask": "255.255.255.192",
        "broadcast": "10.0.1.63",
        "gateway": "10.0.1.1",
        "dhcp_range_start": "10.0.1.10",
        "dhcp_range_end": "10.0.1.62",
        "dns": ["1.1.1.1", "1.0.0.1"],
    },
}


def test_generateDynamicSubnets():
    # Testing with the correct expected subnet sizes (in CIDR notation)
    subnetData, parentNetwork = generateDynamicSubnets(
        networkBase="10.0.0.0/16", numberOfSubnets=5, hostsPerSubnet=50
    )

    assert parentNetwork == "10.0.0.0/16"
    assert len(subnetData) == 5

    # Ensure the generated data matches the expected data
    for subnet, data in subnetData.items():
        assert data == expectedData[subnet]

    # Ensure the function raises a ValueError for too many hosts
    with pytest.raises(ValueError):
        generateDynamicSubnets(
            networkBase="192.168.1.0/24", numberOfSubnets=5, hostsPerSubnet=1000
        )

    # Ensure the function raises a ValueError for an invalid network base
    with pytest.raises(ValueError):
        generateDynamicSubnets(
            networkBase="10.350.0.1", numberOfSubnets=5, hostsPerSubnet=50
        )

    # Ensure the function raises a ValueError for insufficient subnets
    with pytest.raises(ValueError):
        generateDynamicSubnets(
            networkBase="192.168.1.1/24", numberOfSubnets=100, hostsPerSubnet=50
        )
