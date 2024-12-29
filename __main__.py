if __name__ == "__main__":
    import json
    from NG_Subnet import generateDynamicSubnets, DEFAULT_DNS

    networkBasePrompt = (
        "Enter the network base address in CIDR notation (e.g. 10.0.0.0/16): "
    )
    totalSubnetsPrompt = "Enter the total number of subnets: "
    hostsPerSubnetPrompt = "Enter the number of hosts per subnet: "
    overrideDefaultDNSPrompt = "Do you want to change the default DNS servers? (y/n): "
    dnsServersPrompt = "Enter the DNS servers (comma-separated) or 'GATEWAY' to use the gateway as DNS: "

    networkBase: str = input(networkBasePrompt)
    totalSubnets = int(input(totalSubnetsPrompt))
    hostsPerSubnet = int(input(hostsPerSubnetPrompt))
    overrideDefaultDNS: str = input(overrideDefaultDNSPrompt)

    dnsServers: list[str] = (
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
