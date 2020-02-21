import serial
import time

ser = serial.Serial()
ser.baudrate = 115200
ser.port = 'COM1'

ser.open()
ser.write(b'A')

data_str = b''

while True:
    if (ser.inWaiting() > 0):  # if incoming bytes are waiting to be read from the serial input buffer
        # val = ser.read(ser.inWaiting()) # read the bytes and convert from binary array to ASCII
        # if (val == b'0'):
        #     break
        # else :
        data_str += ser.read(ser.inWaiting())


        for i in data_str:
            print('%d;' % i)
        print(len(data_str))

        if ((data_str[4]==0) and (data_str[5]==0) and (data_str[6]==0)):
            print('true')
            break
        # print(data_str, end='')  # print the incoming string without putting a new-line ('\n') automatically after every print()
        # Put the rest of your code you want here
    time.sleep(0.01)  # Optional: sleep 10 ms (0.01 sec) once per loop to let other threads on your PC run during this time.

    if len(data_str) == 4096:
        break
    # tdata = ser.read()           # Wait forever for anything
    # time.sleep(0.3)             # Sleep (or inWaiting() doesn't give the correct value)
    # data_left = ser.inWaiting()  # Get the number of characters ready to be read
    # tdata += ser.read(data_left)
    # if len(tdata)>3200:
    #   break

# print(len(data_str))
# print(data_str)
# for i in data_str:
#     print('%d;' % i)
# s = ser.readline()
# print(len(s))
# for i in s:
#     print('%d;' %i)
# ser.close()