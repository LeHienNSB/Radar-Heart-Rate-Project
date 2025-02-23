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

N = len(Sensor_Data)                  # total number of data points
n = np.arange(0, N, 1)   # trung bình giá trị cyar cột N       
y = Real_Data         # bắt đầu chuỗi np rỗng có N phần tử (vector)
t = np.empty(N)
x = Sensor_Data         # bắt đầu chuỗi np rỗng có N phần tử(vector)
t.fill(80)                # gán giá trị 5 cho toàn bộ cột x (= 5 uM)        
yHat = np.empty(N)       # estimated protein y concentration in uM (vector)
a1Hat = np.empty(N)      # estimated a1 parameter (vector)                                                          
b1Hat = np.empty(N)      # estimated b1 parameter (vector)                                                        
e = np.empty(N)          # y protein estimation error in uM (vector) (= y - yHat)
a1Hat[1] = 0             # initial estimated a1 parameter                                                   
b1Hat[1] = 0            # initial estimated b1 parameter 
u = 0.0001                # step size (mu)

for i in range (1, N-1):                                                    
    yHat[i] = a1Hat[i]*x[i-1] + b1Hat[i]*y[i-1]      # estimated protein y concentration
    e[i] = y[i] - yHat[i]                            # y protein estimation error
    a1Hat[i+1] = a1Hat[i] + u*x[i-1]*e[i]            # estimated a1 parameter
    b1Hat[i+1] = b1Hat[i] + u*y[i-1]*e[i]            # estimated b1 parameter
 
yHat[N-1] = a1Hat[N-1] * x[N-2] + b1Hat[N-1] * y[N-2]                
e[N-1] = y[N-1] - yHat[N-1]     
print (a1Hat[N-1], b1Hat[N-1])                             
plt.plot(n, x, 'r', label = 'x Sensor_Data')                                         
plt.plot(n, y, 'g', label = 'y Real_Data')
plt.plot(n, t, 'g', label = 't test')
plt.plot(n, yHat, 'b', label = 'estimated y Sensor_Data')
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