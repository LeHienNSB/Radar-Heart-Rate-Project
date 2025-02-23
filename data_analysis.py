import pandas as pd
from datetime import datetime
import numpy as np

class BreakLoop(Exception):
    pass

#Đọc file từ sensor
file_path = 'Hien_30_12.csv'  

df = pd.read_csv(file_path)

Time_data = df.iloc[:, 0]
Sensor_Data = df.iloc[:, 1]
Real_Data = df.iloc[:, 8].fillna(0)
Body_Val= df.iloc[:, 7]

for index, time in enumerate(Time_data):
    if(Sensor_Data[index] != 0 and Real_Data[index] != 0):
        start = datetime.strptime(Time_data[index], '%H:%M:%S')
        break  
minuteDeviation = []
sum_Sensor = 0
sum_Real = 0
timeLoop = 0
realLoop = 0

for index, time in enumerate(Time_data):
    time = datetime.strptime(Time_data[index], '%H:%M:%S')

    if(time >= start):
        if(timeLoop <= 1):
            if(Sensor_Data[index] != 0 and Real_Data[index] != 0 and Body_Val[index]<=10 ):
                sum_Sensor += Sensor_Data[index]
                sum_Real += Real_Data[index]
                realLoop += 1
                timeLoop += 1
        if(timeLoop == 1):
            minuteDeviation.append([float(sum_Sensor / realLoop), float(sum_Real / realLoop)])
            sum_Sensor = 0
            sum_Real = 0
            timeLoop = 0
            realLoop = 0

sum_Sensor = 0
sum_Real = 0
newMinuteDevi = []
removeMinuteDevi = []

for i in range(100, -1, -1):
    try:
        for t in range(len(minuteDeviation)):
            if(abs(minuteDeviation[t][1] - minuteDeviation[t][0]) <= i):
                newMinuteDevi.append([minuteDeviation[t][0], minuteDeviation[t][1]])
            if(abs(minuteDeviation[t][1] - minuteDeviation[t][0]) > i):
                removeMinuteDevi.append([minuteDeviation[t][0], minuteDeviation[t][1]])
        for z in range(len(newMinuteDevi)):
            sum_Sensor += newMinuteDevi[z][0]
            sum_Real += newMinuteDevi[z][1]
        if i == 100:
            sum_Sensor_100= sum_Sensor
            sum_Real_100 = sum_Real
            newMinuteDevi_100= newMinuteDevi
        if len(newMinuteDevi)!=0:
            if ((sum_Sensor/len(newMinuteDevi))*100/ (sum_Real/len(newMinuteDevi)))>=90 and ((sum_Sensor/len(newMinuteDevi))*100/ (sum_Real/len(newMinuteDevi)))<=110 and (len(newMinuteDevi)*100/ (len(newMinuteDevi)+len(removeMinuteDevi)))>=80:
                raise BreakLoop
            else:
                sum_Sensor = 0
                sum_Real = 0
                newMinuteDevi=[]
                removeMinuteDevi=[]
        # else:
        #     print("chuỗi rỗng: ",i)
        #    break 
    except BreakLoop:
        if (i!=100):
            print("giá trị chưa lọc:")
            print("  nhịp tim thật:",sum_Real_100/len(newMinuteDevi_100),"/","sensor:",sum_Sensor_100/len(newMinuteDevi_100))
            print("giá trị đã lọc:")
            print("  nhịp tim thật:",sum_Real/len(newMinuteDevi),"/","sensor:",sum_Sensor/len(newMinuteDevi))
        else:
            print("nhịp tim thật:",sum_Real/len(newMinuteDevi),"/","sensor:",sum_Sensor/len(newMinuteDevi))
        print((sum_Sensor/len(newMinuteDevi))*100/ (sum_Real/len(newMinuteDevi)), "%")
        print("Độ Lệch:", i)
        print("Số mẫu còn lại là:",len(newMinuteDevi),"/",(len(newMinuteDevi)+len(removeMinuteDevi)))
        print(len(newMinuteDevi)*100/ (len(newMinuteDevi)+len(removeMinuteDevi)), "%")
        break 
    if(i==0):
        print("đã chạy hết vòng lặp")
        print("  nhịp tim thật:",sum_Real_100/len(newMinuteDevi_100),"/","sensor:",sum_Sensor_100/len(newMinuteDevi_100))
