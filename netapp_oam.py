################################################################################
from acitoolkit.acitoolkit import *
"""
OAM-Netapp OAM

"""
#ten = raw_input(' Enter Tenant name ')
#epg = raw_input(' Enter epg name ')
#bd = raw_input(' Enter BD name ')

# Create the Tenant
tenant = Tenant('common')

# Create the Application Profile
app = AppProfile('Netapp_CIFS', tenant)
app2 = AppProfile('Netapp_NFS', tenant)

# Create the EPG
epg = EPG('EPG1', app)
epg1 = EPG('EPG2', app)
epg2 = EPG('EPG1', app2)
epg3 = EPG('EPG2', app2)



# Create a Context and BridgeDomain
context = Context('Netapp', tenant)
bd = BridgeDomain('Netapp_CIFS', tenant)
bd1 = BridgeDomain('Netapp_NFS', tenant)
bd.add_context(context)

# Place the EPG in the BD
epg.add_bd(bd)
epg1.add_bd(bd)
epg2.add_bd(bd1)
epg3.add_bd(bd1)
"""
# Declare 2 physical interfaces
if1 = Interface('eth', '1', '103', '1', '15')
if2 = Interface('eth', '1', '103', '1', '16')

# Create VLAN 5 on the physical interfaces
vlan5_on_if1 = L2Interface('vlan5_on_if1', 'vlan', '5')
vlan5_on_if1.attach(if1)

vlan5_on_if2 = L2Interface('vlan5_on_if2', 'vlan', '5')
vlan5_on_if2.attach(if2)

# Attach the EPG to the VLANs
epg.attach(vlan5_on_if1)
epg.attach(vlan5_on_if2)
"""
# Get the APIC login credentials
description = 'acitoolkit tutorial application'
creds = Credentials('apic', description)
creds.add_argument('--delete', action='store_true',
                   help='Delete the configuration from the APIC')
args = creds.get()

# Delete the configuration if desired
if args.delete:
    tenant.mark_as_deleted()

# Login to APIC and push the config
session = Session(args.url, args.login, args.password)
session.login()
resp = tenant.push_to_apic(session)
if resp.ok:
    print 'Success'

# Print what was sent
print 'Pushed the following JSON to the APIC'
print 'URL:', tenant.get_url()
print 'JSON:', tenant.get_json()
