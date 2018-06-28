import csv 
from numpy import mean,std
import matplotlib.pyplot as plt


def csvdatawrite(datalist):
	with open("ping64extradata.csv","a",newline='') as csvfile:
		writer = csv.writer(csvfile)
		# 写入多行数据
		writer.writerows(datalist)

csvdata = csv.reader(open("ping64.csv"))
order = 1
temp = 1
reqts = []
rests = []

tempsingledata = []
tempmultidata = []

for row in csvdata:
	if row[0] == "timestamp(microsecond)":
		print(row[0],row[17],row[18],row[19],row[20])
		# print("ignore the column name")

		tempsingledata.append("reqts")
		tempsingledata.append("rests")
		tempsingledata.append("tsminus")
		tempsingledata.append("seq")
		with open("ping64extradata.csv","w",newline='') as csvfile:
			writer = csv.writer(csvfile)
			# 写入列名
			writer.writerow(tempsingledata)
		tempsingledata = []

	else:
		print(row[0],row[17],row[18],row[19],row[20])
		if temp == 1:
			reqts.append(row[0])
			temp = temp + 1
			tempsingledata.append(row[0])
		
		else:
			rests.append(row[0])
			temp = 1
			tempsingledata.append(row[0])
			tempsingledata.append(int(tempsingledata[1])-int(tempsingledata[0]))
			print(tempsingledata[1])
			tempsingledata.append(row[20])
			tempmultidata.append(tempsingledata)
			tempsingledata = []
csvdatawrite(tempmultidata)
# print(reqts)
# print("-----------------------------------------------------------------------")
# print(rests)
tsminus = []  # 所有成对数据包，得时间差
timeminusmean = 0 # 均值
timeminusstd = 0 # 方差

for count in range(len(reqts)):
	# 假设时间点都是匹配的，否则需要匹配他们的id号进行。筛选数据
	tempminus = int(rests[count])-int(reqts[count])
	tsminus.append(tempminus)
timeminusmean = mean(tsminus)
timeminusstd = std(tsminus)
print("mean:",timeminusmean)
# 均值为 5.21
print("std:",timeminusstd)
# 标准差 为 5.05

# 存储正常的 数据req,res和异常的数据 req，res
normalreq = []
normalres = []
abnormalreq = []
abnormalres = []

# 这三种关键字用于作图 
allminus = []
size = []
color = []

# 下一步将 tsminus 之差，大于5的作为 异常点，进行存储，
for count in range(len(reqts)):
	# 假设时间点都是匹配的，否则需要匹配他们的id号进行。筛选数据
	tempminus = int(rests[count])-int(reqts[count])
	allminus.append(tempminus)
	if tempminus> 5:
		size.append(0.5)
		color.append('r')
		abnormalreq.append(reqts[count])
		abnormalres.append(rests[count])
	else:
		size.append(0.5)
		color.append('y')
		normalreq.append(reqts[count])
		normalres.append(rests[count])
# 用时间 差做图 
x = range(1000)
plt.scatter(x[0:100],allminus[0:100],s=size[0:100],c=color[0:100])
print("abnormal points count is:",len(abnormalres))




# 利用req,res预处理后 的值作图 
# x = []
# y = []
# for i in range(len(reqts)):
# 	x.append(int(reqts[i])-1528779048939350)
# 	y.append(int(rests[i])-1528779048939382)
# plt.scatter(x[0:20],y[0:20],s=size[0:20],c=color[0:20])
# plt.scatter(normalreq,normalres,s=0.1,c='r')
# plt.scatter(abnormalreq,abnormalres,s=4,c='y',alpha=0.5)
plt.show()
