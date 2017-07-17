#!/usr/bin/env python
"""
Create OSPF interface
"""

from acitoolkit.acitoolkit import Credentials, Session, Tenant, Context
from acitoolkit.acitoolkit import OutsideL3, OutsideEPG, Interface, L2Interface
from acitoolkit.acitoolkit import L3Interface, OSPFRouter, OSPFInterfacePolicy
from acitoolkit.acitoolkit import OSPFInterface, Contract


def main():
    """
    Main execution routine
    """
    creds = Credentials('apic')
    args = creds.get()
    session = Session(args.url, args.login, args.password)
    session.login()

    tenant = Tenant('common')
    context = Context('OAM_Internet', tenant)
    outside_l3 = OutsideL3('out-1', tenant)
    outside_l3.add_context(context)
    phyif = Interface('eth', '1', '101', '1', '20')
    phyif.speed = '1G'
    l2if = L2Interface('eth 1/101/1/20', 'vlan', '1')
    l2if.attach(phyif)
    l3if = L3Interface('l3if')
    l3if.set_l3if_type('l3-port')
    l3if.set_mtu('1500')
    l3if.set_addr('1.1.1.2/30')
    l3if.add_context(context)
    l3if.attach(l2if)
    rtr = OSPFRouter('rtr-1')
    rtr.set_router_id('23.23.23.23')
    rtr.set_node_id('101')
    ifpol = OSPFInterfacePolicy('myospf-pol', tenant)
    ifpol.set_nw_type('p2p')
    ospfif = OSPFInterface('ospfif-1', router=rtr, area_id='1')
    ospfif.set_area_type('nssa')
    ospfif.auth_key = 'password'
    ospfif.int_policy_name = ifpol.name
    ospfif.auth_keyid = '1'
    ospfif.auth_type = 'simple'
    tenant.attach(ospfif)
    ospfif.networks.append('55.5.5.0/24')
    ospfif.attach(l3if)
    contract1 = Contract('contract-1')
    outside_epg = OutsideEPG('outepg', outside_l3)
    outside_epg.provide(contract1)
    contract2 = Contract('contract-2')
    outside_epg.consume(contract2)
    outside_l3.attach(ospfif)

    print(tenant.get_json())
    resp = session.push_to_apic(tenant.get_url(),
                                tenant.get_json())

    if not resp.ok:
        print('%% Error: Could not push configuration to APIC')
        print(resp.text)

if __name__ == '__main__':
    main()
