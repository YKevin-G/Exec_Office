# -*- coding: UTF-8 -*-
import dpkt
import datetime
import socket
from dpkt.compat import compat_ord
import csv
# import numpy as np
# import time
# np.set_printoptions(suppress=True)


def mac_addr(address):
    """Convert a MAC address to a readable/printable string

       Args:
           address (str): a MAC address in hex form (e.g. '\x01\x02\x03\x04\x05\x06')
       Returns:
           str: Printable/readable MAC address
    """
    return ':'.join('%02x' % compat_ord(b) for b in address)



def inet_to_str(inet):
    """Convert inet object to a string

        Args:
            inet (inet struct): inet network address
        Returns:
            str: Printable/readable IP address
    """
    # First try ipv4 and then ipv6
    try:
        return socket.inet_ntop(socket.AF_INET, inet)
    except ValueError:
        return socket.inet_ntop(socket.AF_INET6, inet)

def csvdata(datalist):
	with open("ping64.csv","a",newline='') as csvfile:
		writer = csv.writer(csvfile)
		# 写入多行数据
		writer.writerows(datalist)


# 创建要存入数据的文件并写入列名
column_name = []
column_name.append("timestamp(microsecond)")

column_name.append("source mac addr")
column_name.append("destiny mac addr")

column_name.append("the version of ip protocol")
column_name.append("header length")
column_name.append("type of operation")
column_name.append("total length of header and data")
column_name.append("identification of every single pkt")
column_name.append("1 repersents more fragment and 0 rp None")
column_name.append("0 represent fragment and 1 represent don't fragment")
column_name.append("reserved unuse")
column_name.append("offset")
column_name.append("time to live")
column_name.append("protocol")
column_name.append("checksum of header")
column_name.append("src ip")
column_name.append("dst ip")

column_name.append("icmp type")
column_name.append("icmp code")
column_name.append("icmp packet id")
column_name.append("icmp packet seq")

column_name.append("source port")
column_name.append("destiny port")
column_name.append("data length")
column_name.append("data checksum")
with open("ping64.csv","w",newline='') as csvfile:
	writer = csv.writer(csvfile)
	# 写入列名
	writer.writerow(column_name)
f = open('icmp64.pcap','rb')
pcap = dpkt.pcap.Reader(f)
count = 0
multidata = []
singledata = []
for ts, buf in pcap:
	# 以纳秒为单位显示时间，一开始得到的时间的单位是秒
	# 1秒 = 1,000毫秒 = 1,000,000微妙 = 1,000,000,000纳秒  = 1,000,000,000,000皮秒 

	# 将时间转化为微秒级别
	tts = ts * 1000000
	data = int(round(tts))
	singledata.append(data)
	print("timestamp(microsecond): ",data)
	# singledata.append(int(round(tts)))
	# print("timestamp(microsecond): ",int(round(tts)))
    # 下面是将时间转化为纳秒级别的
	# print("timestamp(nanosecond): ",int(round(ts * 1000000000)))

	# 得到以太网的数据
	eth = dpkt.ethernet.Ethernet(buf)
	singledata.append(mac_addr(eth.src))
	singledata.append(mac_addr(eth.dst))
	print("source mac addr: ",mac_addr(eth.src))
	print("destiny mac addr: ",mac_addr(eth.dst))
	print("network level protocol: ",eth.type)
	prototype = eth.type
	if (prototype == 2048):  # 只解析被 IPv4 封装的数据
	# 得到网络层数据,并打印出IP头部数据
		ipdata = eth.data
		print("the version of ip protocol: ", ipdata.v)
		print("header length: ", ipdata.hl)
		print("type of operation: ", ipdata.tos)
		print("total length of header and data: ", ipdata.len)  # max 65535
		#  __len__ self.__hdr_len__ + len(self.opts) + len(self.data)
		print("identification of every single pkt: ", ipdata.id)
		print("1 repersents more fragment and 0 rp None: ", ipdata.mf)
		print("0 represent fragment and 1 represent don't fragment: ", ipdata.df)
		print("reserved unuse: ", ipdata.rf)  # 未使用位
		print("offset: ", ipdata.offset)
		print("time to live: ", ipdata.ttl)
		print("protocol: ", ipdata.p)
		print("checksum of header: ", ipdata.sum)
		print("src ip: ", inet_to_str(ipdata.src))
		print("dst ip: ", inet_to_str(ipdata.dst))
		singledata.append(ipdata.v)
		singledata.append(ipdata.hl)
		singledata.append(ipdata.tos)
		singledata.append(ipdata.len)
		singledata.append(ipdata.id)
		singledata.append(ipdata.mf)
		singledata.append(ipdata.df)
		singledata.append(ipdata.rf)
		singledata.append(ipdata.offset)
		singledata.append(ipdata.ttl)
		singledata.append(ipdata.p)
		singledata.append(ipdata.sum)
		singledata.append(inet_to_str(ipdata.src))
		singledata.append(inet_to_str(ipdata.dst))
		# 判断上层协议 是否是 icmp报文
		if (1 == ipdata.p ):
			icmpdata = ipdata.data
			print("icmp type: ",icmpdata.type)
			print("icmp code:", icmpdata.code)
			
			# print (icmpdata.type, icmpdata.code, icmpdata.sum,repr(icmpdata.data))
			echodata = icmpdata.data
			print("icmp packet id :",echodata.id)
			print("icmp packet seq :",echodata.seq)
			singledata.append(icmpdata.type)
			singledata.append(icmpdata.code)
			singledata.append(echodata.id)
			singledata.append(echodata.seq)

			# 获取传输层 数据
			udpdata = dpkt.udp.UDP(echodata.data)
			print("source port: ",udpdata.sport)
			print("destiny port:",udpdata.dport)
			print("data length:",udpdata.ulen)
			print("data checksum: ",udpdata.sum)
			singledata.append(udpdata.sport)
			singledata.append(udpdata.dport)
			singledata.append(udpdata.ulen)
			singledata.append(udpdata.sum)
	# 因为要将数据存入到csv文件中，又因为每次存入一条数据的效率较低，
	# 所以选择每100条存入一次
	# 所使用的存储介质为singledata 用来存储csv文件的一行数据，
	# multidata 用来存储100条 要插入的数据，multidata 由singledata 组成
	# 用 count 来计数100
	if count == 99:
		multidata.append(singledata)  # 现在已经有 100条数据了
		singledata = []
		count = 0
		csvdata(multidata)
		multidata = []
	else:
		multidata.append(singledata)
		singledata = []
		count = count + 1
if len(multidata) > 0:
	csvdata(multidata)
	multidata = []
f.close()