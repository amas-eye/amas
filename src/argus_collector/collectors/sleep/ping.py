#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
ping delay monitoring

A typical ping output:
    64 bytes from 118.178.213.186 (118.178.213.186): icmp_seq=1 ttl=38 time=27.8 ms
    64 bytes from 118.178.213.186 (118.178.213.186): icmp_seq=2 ttl=38 time=142 ms
    64 bytes from 118.178.213.186 (118.178.213.186): icmp_seq=3 ttl=38 time=30.7 ms
    64 bytes from 118.178.213.186 (118.178.213.186): icmp_seq=4 ttl=38 time=49.5 ms
    64 bytes from 118.178.213.186 (118.178.213.186): icmp_seq=5 ttl=38 time=29.0 ms
    
    --- 6ej19t5k0le6q937.alicloudlayer.com ping statistics ---
    5 packets transmitted, 5 received, 0% packet loss, time 4004ms
    rtt min/avg/max/mdev = 27.827/55.970/142.633/44.054 ms
Notes:
    With subprocess.check_out() the response output will append a new line

Compatibility:
    For Py2.6 only
'''

import subprocess as sp
import time

from argus_collector.collectors.etc.ping_conf import *



def main():
    _PACKET_NUM = str(PACKET_NUM)
    _WAIT_TIME = str(WAIT_TIME)
    ts = int(time.time())
    # output = sp.check_output(['ping', '-c', _PACKET_NUM, '-W', _WAIT_TIME, IP])
    result = sp.Popen(['ping', '-c', _PACKET_NUM, '-W', _WAIT_TIME, IP], stdout=sp.PIPE, stderr=sp.PIPE)
    output = result.communicate()[0]
    code = result.returncode
    if code != 0: 
        print 'sys.network.lossrate %s %s' % (ts, 1.00)
        print 'sys.network.rtt %s %s %s' % (ts, -1, 'type=min dest=' + IP)
        print 'sys.network.rtt %s %s %s' % (ts, -1, 'type=avg dest=' + IP)
        print 'sys.network.rtt %s %s %s' % (ts, -1, 'type=max dest=' + IP)
        print 'sys.network.rtt %s %s %s' % (ts, -1, 'type=mdev dest=' + IP)

    else:
        # the last three lines
        summary, rtt, _ = output.split('\n')[-3:]
        
        #construct packet loss rate
        rate_str = summary.split(',')[1]
        rate = 1 - float(rate_str.split()[0]) / float(PACKET_NUM)

        temp_str = '{0:.4f}'.format(rate)
        formatted_rate = float(temp_str)
        print 'sys.network.lossrate %s %s %s' % (ts, formatted_rate, 'dest=' + IP )

        #construct rtt
        result = rtt.split()[3]
        
        type_list = ['min', 'avg', 'max', 'mdev']
        result_list = result.split('/')

        for i in range(len(result_list)):
            tag_field = 'type=%s dest=%s' % (type_list[i], IP)
            print 'sys.network.rtt %s %s %s' % (ts, result_list[i], tag_field )

if __name__ == '__main__':
    main()
