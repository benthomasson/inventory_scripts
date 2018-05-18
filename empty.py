#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Creates a topology of 4 switches.

Usage:
    two_by_two [options]

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
    devices = []

    data['switches'] = devices

    print (json.dumps(data, sort_keys=True, indent=4))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
