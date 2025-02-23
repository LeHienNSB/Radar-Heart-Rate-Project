import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt2
import pandas as pd
from datetime import datetime
np.set_printoptions(precision=15)
file_path = 'Hien1_30_12_test.csv'  

df = pd.read_csv(file_path)
Time_data = df.iloc[:, 2]
Sensor_Data = df.iloc[:, 1]
Real_Data = df.iloc[:, 8].fillna(0)
Body_Val= df.iloc[:, 7]
Respiratory = df.iloc[:, 3]

N = len(Sensor_Data)  
n = np.arange(0, N, 1)                         
y = Real_Data         
x = Sensor_Data         

R = 400
Q = 0.0001
X_hat = np.empty(N)
X_hat[0]= 90
P = 100 + Q
K =0

for i in range (0, N-1):                                                 
    K = P/(P+R)
    X_hat[i] = X_hat[i] + K*(x[i] - X_hat[i])
    X_hat[i+1]= X_hat[i]
    P = (1-K)* P + Q
    print (X_hat)          
plt.plot(n, x, 'r', label = 'x Sensor_Data')                                         
plt.plot(n, X_hat, 'b', label = 'Kalman X')                                                                                 
plt.plot(n, y, 'g', label = 'y Real_Data')
plt.xlabel('time (i)')                                                          
plt.ylabel('protein concentration (uM)')
plt.legend(loc='upper right')
plt.title('LMS Adaptive Filter')
plt.axis([0, N, 0, 150])
plt.grid(True)
plt.show()