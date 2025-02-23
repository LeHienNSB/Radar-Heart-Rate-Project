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
t = np.empty(N)
x = Sensor_Data         
t.fill(80)                   
yHat = np.empty(N)       
a1Hat = np.empty(N)                                                             
b1Hat = np.empty(N)                                                             
e = np.empty(N)          
a1Hat[1] = 0                                                          
b1Hat[1] = 0            
u = 0.0001                     

R = 400
Q = 0.0001
X_hat = np.empty(N)
X_hat[0]= 65
P = 100 + Q
K =0

for i in range (1, N-1):                                                    
    yHat[i] = a1Hat[i]*x[i-1] + 0.46574*65    
    e[i] = 65 - yHat[i]                            
    a1Hat[i+1] = a1Hat[i] + u*x[i-1]*e[i]    
    
for i in range (0, N-1):                                                 
    K = P/(P+R)
    X_hat[i] = X_hat[i] + K*(yHat[i] - X_hat[i])
    X_hat[i+1]= X_hat[i]
    P = (1-K)* P + Q

plt.plot(n, x, 'r', label = 'x Sensor_Data')                                         
plt.plot(n, y, 'g', label = 'y Real_Data')
plt.plot(n, X_hat, 'orange', label = 'KALMAN test')
plt.plot(n, yHat, 'b', label = 'estimated y Real_Data')
plt.plot(n, e, 'y', label = 'y protein estimation error')
plt.xlabel('time (i)')                                                         
plt.ylabel('protein concentration (uM)')
plt.legend(loc='upper right')
plt.title('LMS Adaptive Filter')
plt.axis([0, N,0, 150])
plt.grid(True)
plt.show()

plt2.plot(n, a1Hat, 'm', label = 'estimated a1')
plt2.plot(n, b1Hat, 'c', label = 'estimated b1')
plt2.xlabel('time (i)')                                                         
plt2.ylabel('parameter value')
plt2.legend(loc='upper right')
plt2.title('Estimated Parameter Values')
plt2.axis([0, N, 0, 2])
plt2.grid(True)
plt2.show()