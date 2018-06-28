import csv
from numpy import mean,std

def writereqtesdata(datalist):
	with open("reqtsminusandrestsminus.csv",'a',newline='') as f:
		writer = csv.writer(f)
		# 写入多行数据
		writer.writerows(datalist)
origindata = csv.reader(open("ping64.csv"))
print('have got data',origindata)
reqts = []
reqtsminus = []

rests = []
restsminus = []
column_name = []
column_name.append('reqts')
column_name.append('reqtsminus')
column_name.append('rests')
column_name.append('restsminus')
with open("reqtsminusandrestsminus.csv",'w',newline='') as f:
	writer = csv.writer(f)
	# 写入列名	
	writer.writerow(column_name)
print("file is established")
# 用来计算第一个数据包的时延，也可以理解为是判断第一个数据包的标志
reqtemp = 0
restemp = 0

for row in origindata:
	if (row[0] == "timestamp(microsecond)"):
		print("ignore this message ")
		# pass
	else:
		print("row[1] is this ",row[0])
		if (row[1] == "64:3f:5f:01:56:e8"):
			reqts.append(row[0])
			if(reqtemp == 0):
				reqtsminus.append(0)
				reqtemp = 1 + reqtemp
			else:
				reqtsminus.append(int(row[0])-int(reqts[reqtemp-1]))
				reqtemp = 1 + reqtemp
		else:
			rests.append(row[0])
			if(restemp == 0):
				restsminus.append(0)
				restemp = 1 + restemp
			else:
				restsminus.append(int(row[0])-int(rests[restemp-1]))
				restemp = 1 + restemp
len1 = len(reqts)
len2 = len(rests)
singledata = []
multidata = []
if (len1 == len2):
	for i in range(len1):
		singledata.append(reqts[i])
		singledata.append(reqtsminus[i])
		singledata.append(rests[i])
		singledata.append(restsminus[i])
		multidata.append(singledata)
		singledata = []
elif(len1>len2):
	gap = len1 - len2
	for k in range(gap):
		rests.append("lack of data")
		restsminus.append("lack of data")
	for i in range(len1):
		singledata.append(reqts[i])
		singledata.append(reqtsminus[i])
		singledata.append(rests[i])
		singledata.append(restsminus[i])
		multidata.append(singledata)
		singledata = []
else:
	gap = len2 -len1
	for k in range(gap):
		reqts.append("lack of data")
		reqtsminus.append("lack of data")
	for i in range(len2):
		singledata.append(reqts[i])
		singledata.append(reqtsminus[i])
		singledata.append(rests[i])
		singledata.append(restsminus[i])
		multidata.append(singledata)
		singledata = []
singledata.append("reqtsminus mean")
singledata.append(mean(reqtsminus))
singledata.append("restsminus mean")
singledata.append(mean(restsminus))
multidata.append(singledata)
singledata = []
singledata.append("reqtsminus std")
singledata.append(std(reqtsminus))
singledata.append("restsminus std")
singledata.append(std(restsminus))
multidata.append(singledata)
singledata = []
writereqtesdata(multidata)
