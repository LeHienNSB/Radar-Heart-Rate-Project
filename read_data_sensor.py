import serial
from datetime import datetime

ser = serial.Serial('COM7', baudrate= 115200)

a=[0x00]*20
file=open("HA_19_1.csv", 'w')
x=0
preMinute=0
curMinute=0

while True:
    v=ser.read()
    if v==b'S':
        print(a)
        c=datetime.now()
        preMinute=curMinute
        current_time = c.strftime('%H:%M:%S')
        curMinute=c.minute
        if curMinute!=preMinute:
            file.write("\n\n")
            
        if a[2] == 0x80:
            if a[3] == 0x01:
                if a[6] == 0x00:
                    print(current_time, end=": ")
                    file.write("\t"+current_time+": ")
                    print("NO ONE HERE\n")
                    file.write("NO ONE HERE\n")
                elif a[6] == 0x01:
                    print(current_time, end=": ")
                    file.write("\t"+current_time+": ")
                    print("SOMEONE HERE\n")
                    file.write("SOMEONE HERE\n")
            elif a[3] == 0x02:
                print(current_time, end=": ")
                if a[6]==0x00 or a[6]==0x01 or a[6]==0x02:
                    file.write("\t"+current_time+": ")
                if a[6] == 0x00:
                    print("NO ONE HERE\n")
                    file.write("NO ONE HERE\n")
                elif a[6]==0x01:
                    print("STATIONARY\n")
                    file.write("STATIONARY\n")
                elif a[6]==0x02:
                    print("MOVING\n")
                    file.write("MOVING\n")
            if a[3]==0x03:
                print(current_time, end=": ")
                file.write("\t"+current_time+", ")
                print("BODY VALUE: ", a[6],"\n")
                file.write("BODY VALUE, "+ str(a[6])+"\n")
            elif a[3]==0x04:
                print(current_time, end=": ")
                file.write("\t"+current_time+": ")
                print("DISTANCE: ", a[6]*256+a[7]," cm\n")
                file.write("DISTANCE: "+ str(a[6]*256+a[7])+" cm\n")
            
        elif a[2]==0x85:
            if a[3]==0x02:
                print(current_time, end=": ")
                file.write("\t"+current_time+": ")
                print("HEART RATE: ", a[6]," BPM\n")
                file.write("HEART RATE: "+ str(a[6])+" BPM\n")

        elif a[2]==0x81:
            if a[3]==0x02:
                print(current_time, end=": ")
                file.write("\t"+current_time+", ")
                print("RESPIRATORY RATE: ", a[6]," BPM\n")
                file.write("RESPIRATORY RATE, "+ str(a[6])+" BPM\n")
        a=[0x00]*15
        # b=[]
        x=0
        # ser.write(byte_string)
    a[x]=int.from_bytes(v,'big')
    x=x+1


