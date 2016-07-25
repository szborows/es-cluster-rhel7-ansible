#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import subprocess
import sys

def get_autoscaling_ips(euca_path, autoscaling_group_name):
    p = subprocess.Popen(['scripts/detail/get_ips_for_autoscaling_group {euca_path} {autoscaling_group_name}'.format(euca_path=euca_path, autoscaling_group_name=autoscaling_group_name)], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ips, b = p.communicate()
    if len(b) != 0:
        print('# wtf? {}'.format(b))
    ips = ips.decode('utf-8').split('\n')
    if ips[0].split()[0] == 'eucarc':
        ips = ips[1:]
    return [{'private': x.split()[0], 'public': x.split()[1]} for x in ips if x]


def main(euca_path, autoscaling_group_name, groups):
    ips = get_autoscaling_ips(euca_path, autoscaling_group_name)
    num_requested_nodes = sum([int(e[1]) for e in groups])
    if len(ips) != num_requested_nodes:
        raise RuntimeError('it doesn\'t add up. autoscaling group size: {0}, requested nodes: {1}\n{2}'.format(len(ips), num_requested_nodes, ips))
    inventory_file = ''

    ip_ix = 0
    for ix, group_def in enumerate(groups):
        group_name, num_nodes = group_def
        inventory_file += '[{}]'.format(group_name) + '\n'
        for i in range(int(num_nodes)):
            inventory_file += '{0} ansible_host={1} private_ip={2}\n'.format(
                    group_name + [str(i), ''][int(num_nodes) == 1],
                    ips[ip_ix]['public'],
                    ips[ip_ix]['private'])
            ip_ix += 1
        inventory_file += '\n'
    return inventory_file

if __name__ == '__main__':
    groups = sys.argv[3].split(',')
    groups = [(x.split(':')[0], x.split(':')[1]) for x in groups]
    print(main(sys.argv[1], sys.argv[2], groups))
