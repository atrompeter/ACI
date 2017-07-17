################################################################################
from acitoolkit.acitoolkit import *
"""
OAM-Internet Tenant Space

"""
#ten = raw_input(' Enter Tenant name ')
#epg = raw_input(' Enter epg name ')
#bd = raw_input(' Enter BD name ')

# Create the Tenant
tenant = Tenant('common')

# Create the Application Profile
app = AppProfile('OAM_Internet', tenant)

# Create the EPG
epg = EPG('DNS', app)
epg1 = EPG('AD', app)
epg2 = EPG('LDAP', app)
epg3 = EPG('UNAB', app)
epg4 = EPG('ITIM', app)
epg5 = EPG('McAfee', app)
epg6 = EPG('INFOBLOX' , app)
epg7 = EPG('SEC_MON', app)
epg8 = EPG('APACHER', app)
epg9 = EPG('LAM', app)
epg10 = EPG('bk_Media_Server', app)
epg11 = EPG('OCUM', app)
epg12 = EPG('Jump_Server', app)
epg13 = EPG('KMS', app)
epg14 = EPG('SLM', app)
epg15 = EPG('Safe_Net', app)


# Create a Context and BridgeDomain
context = Context('OAM_Internet', tenant)
bd = BridgeDomain('OAM_Internet', tenant)
bd.add_context(context)

# Place the EPG in the BD
epg.add_bd(bd)

# Define Contracts
contract = Contract('OAM_Internet', tenant)
entry1 = FilterEntry('Entry1',
		     applyToFrag='no',	
                     arpOpc='unspecified',
                     dFromPort='3306',
                     dToPort='3306',
                     etherT='ip',
                     prot='tcp',
                     sFromPort='1',
                     sToPort='65535',
                     tcpRules='unspecified',
                     parent=contract)

#Provide contracts
epg15.provide(contract)
epg14.provide(contract)
epg13.provide(contract)
epg12.provide(contract)
epg11.provide(contract)
epg10.provide(contract)
epg9.provide(contract)
epg8.provide(contract)
epg7.provide(contract)
epg6.provide(contract)
epg5.provide(contract)
epg4.provide(contract)
epg3.provide(contract)
epg2.provide(contract)
epg1.provide(contract)
epg.provide(contract)
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
