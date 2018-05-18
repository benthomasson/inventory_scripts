#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Creates a randomly connect network of a random number of nodes less than 50.

Usage:
    two_by_two [options]

Options:
    -h, --help        Show this page
    --list
    --host=host
"""
import os
import sys
import json
from random import randint


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
    n = os.environ.get('n', 2)
    devices = ['Switch{0}'.format(x) for x in range(n)]

    device_interface_seqs = {name: natural_numbers() for name in devices}
    all_links = set()
    m = os.environ.get('m', 2)

    for name in devices:
        links = []
        for remote_device in devices:
            if (name, remote_device) in all_links:
                continue
            if (remote_device, name) in all_links:
                continue
            if name == remote_device:
                continue
            links.append({'name': 'eth{0}'.format(next(device_interface_seqs[name])),
                          'remote_device_name': remote_device,
                          'remote_interface_name': 'eth{0}'.format(next(device_interface_seqs[remote_device]))
                          })
            all_links.add((name, remote_device))
            all_links.add((remote_device, name))
        host_data = {'ansible_topology': {'type': "switch", 'links': links}}
        data['_meta']['hostvars'][name] = host_data

    data['switches'] = devices

    print (json.dumps(data, sort_keys=True, indent=4))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
