#!/usr/bin/env python3
"""DHCP_Options attach through LSP.dhcpv4_options, not external_ids.ls_uuid."""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import path_tables  # noqa: E402


LS = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
LSP = "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"
DHCP = "cccccccc-cccc-4ccc-8ccc-cccccccccccc"


def test_dhcp_joins_via_lsp_when_external_ids_have_no_ls():
    nb = {
        "Logical_Switch": [{"_uuid": LS, "name": "network_1", "ports": [LSP]}],
        "Logical_Switch_Port": [
            {"_uuid": LSP, "name": "port_1", "type": "", "dhcpv4_options": DHCP}
        ],
        "DHCP_Options": [
            {
                "_uuid": DHCP,
                "cidr": "192.168.2.0/24",
                "options": {"router": "192.168.2.1", "server_mac": "aa:bb:cc:dd:ee:ff", "mtu": "1500"},
                "external_ids": {"foo": "bar"},
            }
        ],
        "Logical_Router": [],
        "Logical_Router_Port": [],
        "Logical_Router_Static_Route": [],
        "NAT": [],
    }
    built = path_tables.build_path_tables(nb, {})
    subnets = built["ovn_subnet"]
    assert len(subnets) == 1, subnets
    row = subnets[0]
    assert row["nb_ls_uuid"] == LS, row
    assert row["nb_cidr"] == "192.168.2.0/24", row
    assert row["nb_gateway_ip"] == "192.168.2.1", row
    assert row["nb_gateway_mac"] == "aa:bb:cc:dd:ee:ff", row
    assert row["nb_mtu"] == 1500, row
    assert row["nb_dhcp_uuid"] == DHCP, row
    switch = built["ovn_switch"][0]
    assert len(switch["subnets"]) == 1, switch["subnets"]
    assert switch["subnets"][0][0] == DHCP


if __name__ == "__main__":
    test_dhcp_joins_via_lsp_when_external_ids_have_no_ls()
    print("ok")
