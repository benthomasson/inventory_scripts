#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage:
    leaf_spine_with_hosts_10000 [options]

Options:
    -h, --help        Show this page
    --list
    --host=host
"""
import sys
import json


def natural_numbers():
    i = 0
    while True:
        yield i
        i += 1

def main(args=None):
    if args is None:
        args = sys.argv[1:]
    if '-h' in args:
        print (__doc__)
        return 1

    if '--host' in args:
        print ("--host not supported")
        return 1

    data = {'_meta': {'hostvars': {}}}
    leaves = ['Leaf{0}'.format(x) for x in range(48)]
    spines = ['Spine{0}'.format(x) for x in range(4)]
    hosts = ['Host{0}-{1}'.format(x, y) for x in range(24) for y in range(440)]
    hosts_per_leaf = {'Leaf{0}'.format(x): ['Host{0}-{1}'.format(x / 2, y) for y in range(440)] for x in range(48)}

    switches = []
    switches.extend(leaves)
    switches.extend(spines)

    devices = []
    devices.extend(leaves)
    devices.extend(spines)
    devices.extend(hosts)

    device_interface_seqs = {name: natural_numbers() for name in devices}

    for name in spines:
        links = []
        host_data = {'ansible_topology': {'type': "switch", 'links': links}}
        data['_meta']['hostvars'][name] = host_data

    for name in leaves:
        links = []
        for remote_device in spines:
            links.append({'name': 'eth{0}'.format(next(device_interface_seqs[name])),
                          'remote_device_name': remote_device,
                          'remote_interface_name': 'eth{0}'.format(next(device_interface_seqs[remote_device]))
                          })
        for remote_device in hosts_per_leaf[name]:
            links.append({'name': 'eth{0}'.format(next(device_interface_seqs[name])),
                          'remote_device_name': remote_device,
                          'remote_interface_name': 'eth{0}'.format(next(device_interface_seqs[remote_device]))
                          })
        host_data = {'ansible_topology': {'type': "switch", 'links': links}}
        data['_meta']['hostvars'][name] = host_data

    for name in hosts:
        links = []
        host_data = {'ansible_topology': {'type': "host", 'links': links}}
        data['_meta']['hostvars'][name] = host_data

    data['switches'] = switches
    data['hosts'] = hosts

    print (json.dumps(data, sort_keys=True, indent=4))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))


