#!/usr/bin/env python
# coding=utf8
"""
/proc/net/dev中的网卡值，需要设置网卡名称

/proc/net/dev文件内容示例：
    [root@fb6c57d65038 new]# cat /proc/net/dev
    Inter-|   Receive                                                |  Transmit
     face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed
      sit0:       0       0    0    0    0     0          0         0        0       0    0    0    0     0       0          0
        lo:       0       0    0    0    0     0          0         0        0       0    0    0    0     0       0          0
    ip6tnl0:       0       0    0    0    0     0          0         0        0       0    0    0    0     0       0          0
    ip6gre0:       0       0    0    0    0     0          0         0        0       0    0    0    0     0       0          0
      eth0:    1296      16    0    0    0     0          0         0      648       8    0    0    0     0       0          0

http://www.onlamp.com/pub/a/linux/2000/11/16/LinuxAdmin.html
字段含义：
bytes       发送或接受的总字节数
packets     发送或接受的报文总数
errs        被设备驱动监测到发送或接受的错误报文总数
drop        由于系统资源限制，被设备驱动丢弃的报文总数
fifo        FIFO 缓存错误数
frame       帧错误数
compressed  发送或接受的压缩报数
multicast   接受到的多播报数
colls       接口检测到的冲突数
carrier     连接介质出现故障次数 , 如 : 网线接触不良
"""
import sys

from argus_collector.collectors.common import *
from argus_collector.collectors.etc.net_dev_conf import *

DATA_PATH = os.path.join(DATA_DIR, 'net_dev.data')
TIME_INTERVAL = os.path.basename(os.path.dirname((os.path.abspath(__file__)))).strip()


def get_by_nic(network_interface_card):
    """
    获取指定网卡设备的流量数据
    :param network_interface_card: 网卡名(字符串或字符串数组）
    :return {
        'card': [ [receive_values], [transmit_values] ],
        ...
    }
    """
    d = {}
    if isinstance(network_interface_card, basestring):
        network_interface_card = [network_interface_card]
    if network_interface_card:
        with open('/proc/net/dev') as f:
            for line in f.readlines():
                line_splited = line.strip().split(':')
                if str(line_splited[0]).strip() in network_interface_card:
                    card_name, values = line_splited
                    value_list = values.strip().split()
                    # {'card': [receive_values], [transmit_values])}
                    d[card_name] = [value_list[0:8], value_list[8:]]
    return d


def main():
    current_time = int(time.time())
    if TIMESTAMP_ALIGN:
        send_time = current_time - current_time % int(TIME_INTERVAL)
    else:
        send_time = current_time

    fields_receive = ['bytes', 'packets', 'errs', 'drop', 'fifo', 'frame', 'compressed', 'multicast']
    fields_transmit = ['bytes', 'packets', 'errs', 'drop', 'fifo', 'colls', 'carrier', 'compressed']

    current_card_values = get_by_nic(NETWORK_INTERFACE_CARD)

    last_data = get_last_data(DATA_PATH)
    if last_data is not None:
        # 上次保存数据的时间戳
        timestamp_last = last_data.keys()[0]
        # 上次保存的数据
        last_card_values = last_data[timestamp_last]
        past_seconds = current_time - int(timestamp_last)

        for card, values in current_card_values.iteritems():
            receive_now, transmit_now = values
            # 如果上次数据中没有该网卡名的值，忽略
            if last_card_values.get(card, None) is not None:
                receive_last, transmit_last = last_card_values.get(card)

                # 计算相对值
                _receive = [(int(_now) - int(_last)) for _now, _last in zip(receive_now, receive_last)]
                _transmit = [(int(_now) - int(_last)) for _now, _last in zip(transmit_now, transmit_last)]

                # 计算每秒平均值
                _receive_persec = [format(float(_) / past_seconds, '0.2f') for _ in _receive]
                _transmit_persec = [format(float(_) / past_seconds, '0.2f') for _ in _transmit]

                # 仅发送配置的网卡字段
                for field, value in zip(fields_receive, _receive_persec):
                    if field in FIELDS['receive']:
                        print('cluster.net.dev.receive {0} {1} type={2} interface={3}'.format(
                            send_time, value, field, card
                        ))
                for field, value in zip(fields_transmit, _transmit_persec):
                    if field in FIELDS['transmit']:
                        print('cluster.net.dev.transmit {0} {1} type={2} interface={3}'.format(
                            send_time, value, field, card
                        ))

        sys.stdout.flush()

    save_data(DATA_PATH, current_card_values, current_time)


if __name__ == '__main__':
    main()
