#!/usr/bin/env python
# -*- coding:utf-8 -*-

from cloudxns.api import *
try:
    import json
except ImportError:
    import simplejson as json

import netifaces as ni
from datetime import datetime

# Configuration
api_key = 'api_key'
secret_key = 'secret_key'
current_interface = 'eth0'
full_domain_name = '1.example.com'
host_name = '1'
domain_id = '12345'
log_storage_path = '/var/log/CloudXNS_DDNS_Script/logs/'
last_ip_configuration_file = '/var/log/CloudXNS_DDNS_Script/last_ip.txt'
ipv6_addr_starts_with = 'bad:c00f:ee'

if __name__ == '__main__':

    print str(datetime.now())

    # get local addresses

    inet4_addresses = []
    for _ in ni.ifaddresses(current_interface)[ni.AF_INET]:
        inet4_addresses.append(_['addr'])

    inet6_addresses = []
    for _ in ni.ifaddresses(current_interface)[ni.AF_INET6]:
        inet6_addresses.append(_['addr'])

    with open(last_ip_configuration_file, 'r') as ipfile:
        ipfile_content_list = ipfile.readlines()

    ipv4_addr_not_changed_flag = False
    ipv6_addr_not_changed_flag = False
    if ipfile_content_list[0].strip() in inet4_addresses:
        print 'IPv4 address didn\'t change'
        inet4_address = ipfile_content_list[0].strip()
        ipv4_addr_not_changed_flag = True
    if ipfile_content_list[1].strip() in inet6_addresses:
        print 'IPv6 address didn\'t change'
        inet6_address = ipfile_content_list[1].strip()
        ipv6_addr_not_changed_flag = True

    # instantiation
    api = Api(api_key=api_key, secret_key=secret_key)

    # --- set up IPv4 record ---

    if not ipv4_addr_not_changed_flag:

        # Determine if there are multiple IPv4 addresses.

        if len(inet4_addresses) > 1:
            print 'Multiple ipv4 addresses found, using the first one.'

        # Use the first ipv4 address to update.

        result = api.ddns(full_domain_name, inet4_addresses[0])

        # Check if IPv4 address updated successfully

        if json.loads(result)['message'] == 'success':
            print 'IPv4 address updated successfully, \
address now is %s' % inet4_addresses[0]
        else:
            print 'IPv4 address failed to update, \
attempted address is %s' % inet4_addresses[0]

        inet4_address = inet4_addresses[0]

    # --- set up IPv6 record ---

    if not ipv6_addr_not_changed_flag:

        # get host list and get record_id for host name

        records_list = json.loads(api.record_list(domain_id))
        for record in records_list['data']:
            if record['host'] == host_name and record['type'] == 'AAAA':
                record_id = int(record['record_id'])
                break

        print 'Updating AAAA record, using the address starting with\
 %s.' % ipv6_addr_starts_with
        inet6_address = ''
        for i6address in inet6_addresses:
            if i6address.startswith(ipv6_addr_starts_with):
                inet6_address = i6address
                break

        if inet6_address == '':
            inet6_address = inet6_addresses[0]

        result = api.record_update(
            record_id, domain_id, host_name, inet6_address,
            record_type='AAAA', mx=None, ttl=600,
            line_id=1, spare_data=None)

        if json.loads(result)['message'] == 'success':
            print 'IPv6 address updated successfully, \
            address now is %s' % inet6_address
        else:
            print 'IPv6 address failed to update, \
            attempted address is %s' % inet6_address

    with open(last_ip_configuration_file, 'w') as ipfile:
        ipfile_content = inet4_address + '\n' + inet6_address + '\n'
        ipfile.write(ipfile_content)
