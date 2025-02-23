import pandas as pd
from datetime import datetime
import numpy as np
np.set_printoptions(precision=15)
# Đọc file CSV
file_path = 'Hien_30_12.csv'  

df = pd.read_csv(file_path)
Time_data = df.iloc[:, 2]
Sensor_Data = df.iloc[:, 1]
Real_Data = df.iloc[:, 8].fillna(0)
Body_Val= df.iloc[:, 7]
Respiratory = df.iloc[:, 3]

for index, time in enumerate(Time_data):
    if(Sensor_Data[index] != 0 and Respiratory[index] != 0):
        start = datetime.strptime(Time_data[index], '%H:%M:%S')
        break  
minuteDeviation = []
sum_Sensor = 0
sum_Respiratory = 0
timeLoop = 0
realLoop = 0

for index, time in enumerate(Time_data):
    time = datetime.strptime(Time_data[index], '%H:%M:%S')

    if(time >= start):
        if(timeLoop <= 1 ):
            if(Sensor_Data[index] != 0 and Real_Data[index] != 0 and Respiratory[index] != 0 and Body_Val[index]<=200 ):
                sum_Sensor += Sensor_Data[index]
                sum_Respiratory += Respiratory[index]
                realLoop += 1
                timeLoop += 1
        if(timeLoop == 1):
            minuteDeviation.append([float(sum_Sensor / realLoop), float(sum_Respiratory / realLoop)])
            sum_Sensor = 0
            sum_Respiratory = 0
            timeLoop = 0
            realLoop = 0

sum_Sensor = 0
sum_Respiratory = 0
newMinuteDevi = []
removeMinuteDevi = []


for i in range(len(minuteDeviation)):
    if(abs(minuteDeviation[i][1] - minuteDeviation[i][0]) <=100):
        newMinuteDevi.append([minuteDeviation[i][0], minuteDeviation[i][1]])
    if(abs(minuteDeviation[i][1] - minuteDeviation[i][0]) > 100):
        removeMinuteDevi.append([minuteDeviation[i][0], minuteDeviation[i][1], i+1 ])
    

for i in range(len(newMinuteDevi)):
    sum_Sensor += newMinuteDevi[i][0]
    sum_Respiratory += newMinuteDevi[i][1]

Respiratory_SensorHR =0
for i in range(len(newMinuteDevi)-1):
    if (((newMinuteDevi[i][0] - newMinuteDevi[i+1][0]>0) and (newMinuteDevi[i][1]-newMinuteDevi[i+1][1]>0)) or ((newMinuteDevi[i][0] - newMinuteDevi[i+1][0]<0) and (newMinuteDevi[i][1]-newMinuteDevi[i+1][1]<0)) or ((newMinuteDevi[i][0] - newMinuteDevi[i+1][0]==0) and (newMinuteDevi[i][1]-newMinuteDevi[i+1][1]==0))):
        Respiratory_SensorHR = Respiratory_SensorHR + 1
# for i in range(len(newMinuteDevi)-1):
#     if (((newMinuteDevi[i][0] - newMinuteDevi[i+1][0]>0) and (newMinuteDevi[i][1]-newMinuteDevi[i+1][1]>0)) or ((newMinuteDevi[i][0] - newMinuteDevi[i+1][0]<0) and (newMinuteDevi[i][1]-newMinuteDevi[i+1][1]<0))):
#         Respiratory_SensorHR = Respiratory_SensorHR + 1
print(newMinuteDevi)
print(sum_Sensor/len(newMinuteDevi),"/", sum_Respiratory/len(newMinuteDevi))
print (Respiratory_SensorHR*100/len(newMinuteDevi),"%")
