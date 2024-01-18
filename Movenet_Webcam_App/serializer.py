import serial, time

ser = serial.Serial()
ser.baudrate = 115200
ser.port = 'COM3'
ser.open()
print('serial open - ')
print(ser.is_open)
input_value = 1000

incommingBYTES = ser.inWaiting()
print('incomming BYTES 1')
print(incommingBYTES)
inBytes = ser.read(incommingBYTES)
print(inBytes)

packet = ''
counter = 0
index = -1

while (True):
    userIn = input()
    ser.write(('<' + userIn + '>').encode())
    # ser.write(userIn.encode(encoding = 'ascii'))
    # ser.write(packet)

    incommingBYTES = ser.inWaiting()
    print('incomming BYTES 1')
    print(incommingBYTES)
    inBytes = ser.read(incommingBYTES)
    print(inBytes)
    
while (index < 5):
    index+=1
    input_value += 1234
    counter += 1
    packet = ' ' + str(input_value) + ' ' + str(input_value + 3) + ' ' + str(input_value + 7) + ' ' + str(input_value + 10) + ' '
    print('sending ' + packet)
    ser.write(packet.encode(encoding = 'ascii'))
    # ser.write(packet)

    incommingBYTES = ser.inWaiting()
    print('incomming BYTES 1')
    print(incommingBYTES)
    inBytes = ser.read(incommingBYTES)
    print(inBytes)
    
    time.sleep(1/30)
    print()

    # incommingBYTES = ser.inWaiting()
    # print('incomming BYTES 2')
    # print(incommingBYTES)
    # inBytes = ser.read(incommingBYTES)
    # print(inBytes)
    # if counter % 3 == 0:
    #     print()
    #     print()
    #     time.sleep(15)
    #     print()
    #     print()