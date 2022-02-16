from os import environ, path, mkdir
from json import dumps
import sys
from subprocess import getoutput
from re import search

home = environ.get('HOME')

if not home:
    print('Alert: HOME variable not set exiting...')
    exit()

if __name__ == '__main__':
    if len(sys.argv)==1:
        print('Error: an ip is needed exiting')
        exit(1)
    target = sys.argv[1]
    output = getoutput('ifconfig')
    output = output.split("\n\n")
    eth0 = tun0 = ''
    for interface in output:
        if interface.startswith('tun0'):
            tun0 = search(r"(?:inet \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", interface)
            if tun0:
                tun0 = tun0.group()[5:]
        if interface.startswith('eth0'):
            eth0 = search(r"(?:inet \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", interface)
            if eth0:
                eth0 = eth0.group()[5:]
    config = {'tun0':tun0, 'target': target, 'eth0':eth0}
    if not path.exists(home + '/.config/misterbug5/'):
        mkdir(home + '/.config/misterbug5/')
    file = open(home + '/.config/misterbug5/ip.json', 'w')
    file.write(dumps(config))
    file.close()
