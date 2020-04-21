#/usr/bin/env python
#
# This sample shows how to connect to an APIC and retrieve all instances of an ACI object class.
# The object class fvTenant is uses as an example.
#
import requests
import json
import sys
import urllib3
import argparse
import getpass
from pprint import pprint as pp
# Suppress insecure cert warnings etc
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecurePlatformWarning)
urllib3.disable_warnings(urllib3.exceptions.SNIMissingWarning)
# Arg parser with one mandatory, positional argument
parser = argparse.ArgumentParser(description="Network info script.")
parser.add_argument("apic", help="Hostname or IP address of APIC.")
# Collect args
args = parser.parse_args()
# Allow user to enter APIC name/IP address with or without leading https://
if args.apic.startswith('https'):
    apic_address = args.apic
else:
    apic_address = 'https://' + args.apic
# Prompt for APIC username and password
apic_user = input("ACI Username: ")
apic_password = getpass.getpass(prompt="ACI Password: ")
# Construct HTTP headers, payload and login uri
headers = {'content-type': "application/json", 'cache-control': "no-cache"}
login_uri = '{0}/api/aaaLogin.json'.format(apic_address)
payload = {'aaaUser': {'attributes': {'name': apic_user, 'pwd': apic_password}}}
response = requests.post(login_uri, data=json.dumps(payload), headers=headers, verify=False)
# Print HTTP response code
print('Login response code:', response.status_code)
# Save cookie for following commands
cookie = {'APIC-cookie': response.cookies['APIC-cookie']}
# Builduri to collect all fvTenant objects
tenant_uri = '{0}/api/class/fvTenant.json'.format(apic_address)
response = requests.get(tenant_uri, headers=headers, cookies=cookie, verify=False)
# response.json() should look something like this:
#
#{'imdata': [{'fvTenant': {'attributes': {'annotation': 'orchestrator:msc',
#                                         'childAction': '',
#                                         'descr': '',
#                                         'dn': 'uni/tn-David-Tenant',
#                                         'extMngdBy': 'msc',
#                                         'lcOwn': 'local',
#                                         'modTs': '2019-10-21T13:51:37.773+01:00',
#                                         'monPolDn': 'uni/tn-common/monepg-default',
#                                         'name': 'David-Tenant',
#                                         'nameAlias': '',
#                                         'ownerKey': '',
#                                         'ownerTag': '',
#                                         'status': '',
#                                         'uid': '9648'}}},
#            {'fvTenant': {'attributes': {'annotation': 'orchestrator:msc',
#                                         'childAction': '',
#                                         'descr': '',
#                                         'dn': 'uni/tn-Neil-Tenant',
#                                         'extMngdBy': '',
#                                         'lcOwn': 'local',
#                                         'modTs': '2019-10-21T10:20:41.363+01:00',
#                                         'monPolDn': 'uni/tn-common/monepg-default',
#                                         'name': 'Neil-Tenant',
#                                         'nameAlias': '',
#                                         'ownerKey': '',
#                                         'ownerTag': '',
#                                         'status': '',
#                                         'uid': '9648'}}}],
#'totalCount': '2'}
#
# Use pretty print to check reults:
#pp(response.json())
#
# response.json()['imdata'] is a list of fvTenants, so iterate over it:
for tenant in response.json()['imdata']:
    name = tenant['fvTenant']['attributes']['name']
    print('Tenant name:', name)
