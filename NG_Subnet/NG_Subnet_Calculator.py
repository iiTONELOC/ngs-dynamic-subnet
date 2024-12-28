"""
Copyright (c) 2024 Anthony Tropeano
All Rights Reserved.

Description: This script generates dynamic subnets based on the provided network base
             address and parameters.
"""

import ipaddress
from typing import Literal

# Defaults to Cloudflare DNS servers
DEFAULT_DNS: list[str] = ["1.1.1.1", "1.0.0.1"]


def calculateRequiredSubnetSize(hostsPerSubnet: int) -> int:
    """
    Determine the subnet mask needed to accommodate the given number of hosts per subnet.
    The subnet must also accommodate the reserved addresses (e.g., network, gateway).
    """
    # Include reserved addresses (network and broadcast) in the total address count.
    requiredAddresses = hostsPerSubnet + 2  # network + broadcast addresses

    # Loop through all possible subnet masks from /32 to /0.
    for mask in range(32, 0, -1):
        # Calculate the total number of addresses for the current subnet mask.
        totalAddresses = 2 ** (32 - mask)

        # Check if the total number of addresses is enough to accommodate the required number of addresses.
        if totalAddresses >= requiredAddresses:
            return mask

    raise ValueError(
        "Unable to calculate subnet mask for the given number of hosts per subnet."
    )


def generateDynamicSubnets(
    networkBase: str,
    numberOfSubnets: int,
    hostsPerSubnet: int,
    dnsServers: list[str] | Literal["GATEWAY"] = DEFAULT_DNS,
) -> tuple[dict, str]:
    """Generate dynamic subnets based on the provided network base address and parameters.

    Args:
        networkBase (str): The base network address in CIDR notation (e.g., '10.0.0.0/16').
        numberOfSubnets (int): The number of subnets to generate.
        hostsPerSubnet (int): The number of hosts required per subnet.
        dnsServers (list[str] | Literal[&quot;GATEWAY&quot;], optional):A comma separated list of DNS servers. Defaults to DEFAULT_DNS.

    Raises:
        ValueError: If the network base address is invalid.
        ValueError: If there are insufficient subnets available for the requested configuration.
        ValueError: If a subnet does not have enough usable addresses after reserving space.
        ValueError: If the DHCP range in a subnet is invalid.

    Returns:
        tuple[dict, str]: A tuple containing the generated subnet data and the parent network address.
    """

    subnetData: dict = {}
    requiredSubnetMask: int = calculateRequiredSubnetSize(hostsPerSubnet=hostsPerSubnet)

    # Ensure networkBase is in the correct CIDR format
    if "/" not in networkBase:  # If it's not in CIDR format like '10.0.0.0/8'
        networkBase = f"{networkBase}/24"  # Default to /24 if no CIDR is provided

    # Try to create the parent network from the base address
    try:
        parentNetwork = ipaddress.IPv4Network(networkBase, strict=False)
    except ValueError as e:
        raise ValueError(f"Invalid network base address: {networkBase}. Error: {e}")

    # Check if we have enough subnets
    subnets = list(parentNetwork.subnets(new_prefix=requiredSubnetMask))
    if len(subnets) < numberOfSubnets:
        raise ValueError(
            "Insufficient subnets available for the requested configuration."
        )

    # Generate subnet data
    for i in range(numberOfSubnets):
        subnet = subnets[i]
        usableHosts = list(subnet.hosts())

        # Ensure there are enough usable hosts for the requested DHCP range
        if len(usableHosts) < hostsPerSubnet:
            raise ValueError(
                f"Subnet {subnet} does not have enough usable addresses after reserving space."
            )

        # Skip 15% of the usable space for static/reserved addresses
        reservedHosts = int(0.15 * len(usableHosts))
        dhcpRangeStart: ipaddress.IPv4Address = usableHosts[reservedHosts]
        dhcpRangeEnd: ipaddress.IPv4Address = usableHosts[-1]

        # Ensure that DHCP range is valid
        if dhcpRangeStart >= dhcpRangeEnd:
            raise ValueError(
                f"Invalid DHCP range in subnet {subnet}. Adjust your hosts per subnet or reserved addresses."
            )

        # the first usable host will be the gateway
        gateway = usableHosts[0]
        # check for DNS servers, if 'GATEWAY' is in the list or the list is 'GATEWAY', use the gateway as DNS
        wantsGatewayDns = "GATEWAY" in dnsServers or dnsServers == "GATEWAY"
        resolvedDns = [str(gateway)] if wantsGatewayDns else dnsServers

        # Store the subnet data in the dictionary
        subnetData[f"Subnet-{i + 1}"] = {
            "subnet": str(subnet),
            "usable_range": f"{usableHosts[0]} - {usableHosts[-1]}",
            "netmask": str(subnet.netmask),
            "broadcast": str(subnet.broadcast_address),
            "gateway": str(gateway),
            "dhcp_range_start": str(dhcpRangeStart),
            "dhcp_range_end": str(dhcpRangeEnd),
            "dns": resolvedDns,
        }

    return subnetData, str(parentNetwork)


if __name__ == "__main__":
    import json

    networkBasePrompt = (
        "Enter the network base address in CIDR notation (e.g. 10.0.0.0/16): "
    )
    totalSubnetsPrompt = "Enter the total number of subnets: "
    hostsPerSubnetPrompt = "Enter the number of hosts per subnet: "
    overrideDefaultDNSPrompt = "Do you want to change the default DNS servers? (y/n): "
    dnsServersPrompt = "Enter the DNS servers (comma-separated) or 'GATEWAY' to use the gateway as DNS: "

    networkBase = input(networkBasePrompt)
    totalSubnets = int(input(totalSubnetsPrompt))
    hostsPerSubnet = int(input(hostsPerSubnetPrompt))
    overrideDefaultDNS = input(overrideDefaultDNSPrompt)

    dnsServers = (
        input(dnsServersPrompt).split(",")
        if overrideDefaultDNS.lower()[0] == "y"
        else DEFAULT_DNS
    )

    # Generate the subnet data and return the results, parent network, and subnet mask
    subnetData, parentNetwork = generateDynamicSubnets(
        networkBase=networkBase,
        numberOfSubnets=totalSubnets,
        hostsPerSubnet=hostsPerSubnet,
        dnsServers=dnsServers,
    )

    print("\nParent Network: ", parentNetwork)
    print("Subnet Data:\n", json.dumps(subnetData, indent=4))
