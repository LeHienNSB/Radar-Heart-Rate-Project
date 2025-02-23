import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt2
import pandas as pd
from datetime import datetime
file_path = 'Hien1_30_12_test.csv'  

df = pd.read_csv(file_path)
Time_data = df.iloc[:, 2]
Sensor_Data = df.iloc[:, 1]
Real_Data = df.iloc[:, 8].fillna(0)
Body_Val= df.iloc[:, 7]
Respiratory = df.iloc[:, 3]

N = len(Sensor_Data)                  # total number of data points
n = np.arange(0, N, 1)   # trung bình giá trị cyar cột N       
#y = Real_Data         # bắt đầu chuỗi np rỗng có N phần tử (vector)
t = np.empty(N)
x = Sensor_Data         # bắt đầu chuỗi np rỗng có N phần tử(vector)

def rls_filter(N, d, delta=1.0, lambda_=0.99):
    """Bộ lọc RLS với tham số giảm λ và hệ số khởi tạo delta"""
    M = 4  # Kích thước bộ lọc
    
    w = np.zeros(M)  # Trọng số bộ lọc ban đầu
    P = np.eye(M) * delta  # Ma trận hiệp phương sai
    
    y = np.zeros(N)  # Tín hiệu đầu ra
    e = np.zeros(N)  # Sai số
    
    for n in range(M, N):
        X = x[n-M:n][::-1]  # Vector đầu vào
        pi = P @ X  # Vector trung gian
        K = pi / (lambda_ + X.T @ pi)  # Gain vector
        
        y[n] = np.dot(w, X)  # Dự đoán đầu ra
        e[n] = d[n] - y[n]  # Sai số
        
        w += K * e[n]  # Cập nhật trọng số
        P = (P - np.outer(K, pi)) / lambda_  # Cập nhật ma trận P
    
    return y, e, w

y, e, w = rls_filter(N, x)

# Hiển thị kết quả
plt.plot(x, label="Desired Signal (d)")
plt.plot(y, label="Filtered Signal (y)")
plt.legend()
plt.title("RLS Filtering")
plt.show()