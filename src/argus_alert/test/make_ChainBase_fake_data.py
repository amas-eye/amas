# coding= utf-8
import socket
import json
import time


host = '192.168.0.253' # OPENTSDB_HOST
port = 4242         # OPENTSDB_PORT


def getTimeOClockOfToday():
    t = time.localtime(time.time())
    time1 = time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00', t),'%Y-%m-%d %H:%M:%S'))
    return int(time1)

def send_to_tsd(s, metric,ts,value,tag):
	# md = {
    # "metric": metric,
    # "timestamp": ts,
    # "value": value,
    # "tags": {
    #    "host": tag
    # 	}
	# }
	item = f'put {metric} {ts} {value} {tag}\n'
	# jsmd = json.dumps(md)
	# print(jsmd)
	p_item = bytes(item,'utf-8')
	# s.send(p_item)
	return item


if __name__ == "__main__":
	sock = socket.socket()
	# sock.bind(host=host,port=port)
	sock_tuple = (host, port)
	sock.connect(sock_tuple)
	metric_values = [
		('test.increse.rate',130),
		('test.decrese.rate',70),
		# ('test.increse.rate',100),
		# ('test.decrese.rate',100)
	]
	# insert_before_time = False
	insert_before_time = True
	today_start_time = getTimeOClockOfToday()
	print(today_start_time)
	if insert_before_time == True:
		today_start_time = today_start_time - (7 * 24 * 60 * 60)
	interval = 300
	insert_times = int((24 * 60 * 60) / interval)
	send_data = ''
	for i in range(insert_times):
		check_time = today_start_time + (interval * i)
		for item in metric_values:
			sen = send_to_tsd(sock, item[0],check_time,item[1],"host=TESTHOST")
			send_data += sen
	s_s = bytes(send_data,'utf-8')
	sock.sendall(s_s)