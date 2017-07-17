#!/usr/bin/env python
"""
It logs in to the APIC and will create a VMM Domain.

NOTE:  additional configuration is likely required, as the newly created VMM domain will need to be associated
with an AEP for the ESX hosts, as well as attaching the ESX hosts to the DVS.

"""
import acitoolkit.acitoolkit as aci

# Define static values to pass, these can be dymanic using raw_input 

VMM_TYPE = 'VMware'
DVS_NAME = 'aci-test-dvs'
ACI_USER = 'admin'
ACI_PASS = 'password'
APIC_IP = 'http://apic'
DATACENTER_NAME = 'DATACENTER'  # Must match the data center name in vCenter
VCENTER_IP = '1.1.1.1'
VCENTER_USER = 'administrator'
VCENTER_CREDS = VCENTER_USER
VCENTER_PASS = 'P@ssw0rd'
POOL_NAME = 'dvs-vlans'
ENCAP_TYPE = 'vlan'
VLAN_START = '3150'
VLAN_END = '3200'
POOL_MODE = 'dynamic'


def main():
    """
    Main create VMM routine
    :return: None
    """
    # Get all the arguments
    description = 'Create VMM Domain'
    creds = aci.Credentials('apic', description)
    args = creds.get()

    # Login to the APIC
    session = aci.Session(args.url, args.login, args.password)
    resp = session.login()
    if not resp.ok:
        print('%% Could not login to APIC')

    # Define dynamic vlan range
    vlans = aci.NetworkPool(POOL_NAME, ENCAP_TYPE, VLAN_START, VLAN_END, POOL_MODE)

    # Commit VLAN Range
    vlanresp = session.push_to_apic(vlans.get_url(), vlans.get_json())

    if not vlanresp.ok:
        print('%% Error: Could not push configuration to APIC')
        print(vlanresp.text)

    # Create Credentials object
    vcenter_creds = aci.VMMCredentials(VCENTER_CREDS, VCENTER_USER, VCENTER_PASS)

    # Vswitch Info object
    vswitch_info = aci.VMMvSwitchInfo(VMM_TYPE, DATACENTER_NAME, DVS_NAME)

    # Create VMM object
    vmm = aci.VMM(DVS_NAME, VCENTER_IP, vcenter_creds, vswitch_info, vlans)

    # Commit Changes
    resp = session.push_to_apic(vmm.get_url(), vmm.get_json())

    if not resp.ok:
        print('%% Error: Could not push configuration to APIC')
        print(resp.text)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
