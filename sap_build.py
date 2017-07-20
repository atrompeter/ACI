################################################################################
from acitoolkit.acitoolkit import *
"""
SAP_Build

"""
#ten = raw_input(' Enter Tenant name ')
#epg = raw_input(' Enter epg name ')
#bd = raw_input(' Enter BD name ')

# Create the Tenant
tenant = Tenant('SAP')

# Create the Application Profile
app = AppProfile('Prod', tenant)
app1 = AppProfile('NON-Prod' , tenant)
app2 = AppProfile('QA' , tenant)

# Create the EPG
epg = EPG('client', app)
epg1 = EPG('DB', app)
epg2 = EPG('WEB', app)
epg3 = EPG('Internode', app)
epg4 = EPG('App_Serv_Net', app)
epg5 = EPG('Replication', app)
epg6 = EPG('Back_Up' , app)
epg7 = EPG('MISC', app)


# Create a Context and BridgeDomain
context = Context('Prod', tenant)
bd = BridgeDomain('Client_Zone', tenant)
bd1 = BridgeDomain('Internal_Zone', tenant)
bd2 = BridgeDomain('Storage_Zone', tenant)
bd.add_context(context)
bd1.add_context(context)
bd2.add_context(context)

# Place the EPG in the BD
epg.add_bd(bd)
epg1.add_bd(bd)
epg2.add_bd(bd)
epg3.add_bd(bd1)
epg4.add_bd(bd1)
epg5.add_bd(bd1)
epg6.add_bd(bd2)
"""
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
#epg7.provide(contract)
#epg6.provide(contract)
#epg5.provide(contract)
#epg4.provide(contract)
#epg3.provide(contract)
#epg2.provide(contract)
#epg1.provide(contract)
#epg.provide(contract)
"""
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
