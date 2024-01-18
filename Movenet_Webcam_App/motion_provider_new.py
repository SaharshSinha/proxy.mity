from math import sin, cos, radians, pi, atan2, degrees, dist
from body_points import BodyPoint, BodyPointColor, color_array
import motioner
import cv2
import serial
from playsound import playsound

ser = serial.Serial()
ser.baudrate = 115200
ser.port = 'COM4'
ser.open()
print('serial open - ')
print(ser.is_open)
hasnt_moved_yet = True
_X_ = 0
_Y_ = 1

_VALUE_1_OFFSET = 12500
_VALUE_2_OFFSET = 17500
_VALUE_3_OFFSET = 22500
_VALUE_4_OFFSET = 27500

stabilizer_len = 6
acceptable_range = 1
tolerance = 40

_BASE_MARK = 10000
_BASE_MARK_LEFT = 10001
_BASE_MARK_RITE = 10002
_BASE_MARK_X_RT = 10003
_BASE_MARK_Y_RT = 10004

_BASE_SPEED_LEFT = 1
_BASE_SPEED_RITE = 1
_BASE_SPEED_X_RT = 1
_BASE_SPEED_Y_RT = 1

class PreviousMux: 
    mux_X_prev = 0
    mux_Y_prev = 0

track_points = True
move_camera = track_points and True
move_robot =True

prev = PreviousMux()

class TrackerPointStabilizerX:
    stabilization_length = 3
    points = []
    sum_total = 0
    value = 0
    _delta_threshold = 10
    _prev_point = 0
    def add_point(self, point):
        self.sum_total += point
        self.points.append(point)
    
        if len(self.points) > self.stabilization_length:
            self.sum_total -= self.points.pop(0)
        self.value = round(self.sum_total /  len(self.points))

class TrackerPointStabilizerY:
    stabilization_length = 3
    points = []
    sum_total = 0
    value = 0
    _delta_threshold = 10
    _prev_point = 0

    def add_point(self, point):
        self.sum_total += point
        self.points.append(point)
        
        if len(self.points) > self.stabilization_length:
            self.sum_total -= self.points.pop(0)
        self.value = round(self.sum_total /  len(self.points))

stabilizerX = TrackerPointStabilizerX()
stabilizerY = TrackerPointStabilizerY()

def initialize_steppers():
    write_serial_strings(_BASE_MARK, _BASE_MARK, _BASE_MARK_LEFT, _BASE_SPEED_LEFT)
    write_serial_strings(_BASE_MARK, _BASE_MARK, _BASE_MARK_RITE, _BASE_SPEED_RITE)
    write_serial_strings(_BASE_MARK, _BASE_MARK, _BASE_MARK_X_RT, _BASE_SPEED_X_RT)
    write_serial_strings(_BASE_MARK, _BASE_MARK, _BASE_MARK_Y_RT, _BASE_SPEED_Y_RT)

def write_text(idx, height, img, text):
    return cv2.putText(
        img, 
        text, 
        (10, height + (idx * 20)), 
        cv2.FONT_HERSHEY_SIMPLEX, 
        0.5, 
        (255, 0, 0), 
        1, 
        cv2.LINE_AA)


def move_it(pose_points, body_point, img, width, height):
    xMid = round(width / 2)
    yMid = round(height / 2)
    img = cv2.circle(img, (xMid, yMid), 1, (0, 0, 255), 2)
    if (len(pose_points) < 3):
        write_serial_string(_VALUE_1_OFFSET)
        write_serial_string(_VALUE_2_OFFSET)
        img = write_text(0, 100, img, 'only seeing ' + str(len(pose_points)) + ' points')
        return img
    try:
        mux_X = -1
        mux_Y = -1
        mux_left = -1
        mux_rite = -1
        value_to_write_X = -1
        value_to_write_Y = -1
        # MOVE CAMERA
        if track_points: 
            target_point = pose_points[body_point.value]
            xPos = target_point[_X_] + (-1 * 7 * motioner.direction)
            yPos = target_point[_Y_] + 5
            min_limit_X = xMid - acceptable_range
            max_limit_X = xMid + acceptable_range
            min_limit_Y = yMid - acceptable_range
            max_limit_Y = yMid + acceptable_range
            img = cv2.circle(img, target_point, 1, (0, 0, 0), 2)
            img = cv2.rectangle(
                    img, 
                    (min_limit_X, min_limit_Y), 
                    (max_limit_X, max_limit_Y), 
                    (100, 100, 100),
                    1)  
            
            mux_X = getAdjustedValue(xPos, xMid)
            if (prev.mux_X_prev != mux_X):
                stabilizerX.add_point(mux_X)
                mux_X = stabilizerX.value
                value_to_write_X = mux_X + _VALUE_1_OFFSET
                if move_camera: 
                    write_serial_string(value_to_write_X)
                prev.mux_X_prev = mux_X 

            mux_Y = getAdjustedValue(yPos, yMid)
            if (prev.mux_Y_prev != mux_Y):
                # stabilizerY.add_point(mux_Y)
                # mux_Y = stabilizerY.value
                value_to_write_Y = mux_Y + _VALUE_2_OFFSET
                if move_camera: 
                    write_serial_string(value_to_write_Y)
                prev.mux_Y_prev = mux_Y 
            print ('mux_X:', mux_X, 'value_to_write_X:', value_to_write_X, 'prev.mux_X_prev', prev.mux_X_prev)
        # MOVE ROBOT 
        move_the_robot(move_robot)

        message_to_send = f'{mux_X} ({value_to_write_X}) {mux_Y} ({value_to_write_Y}) {mux_left} {mux_rite}'
        print(message_to_send)
        img = write_text(0, 100, img, message_to_send)
        # write_serial_string(message_to_send)
        # write_serial_strings(mux_X*10, mux_Y*10, 0, 0)
        read_serial()
    
    except Exception as e: 
        print('error in move_it', e)
    return img

def move_the_robot(its_ok_to_move):
    motioner.get_instructions()
    instructions = motioner.next_instructions 
    if motioner.hasnt_moved_yet and (instructions[1] != 0 or instructions[2] != 0):
        motioner.hasnt_moved_yet = False 
        playsound('C:\\Windows\\Media\\tada.wav')
    mux_left = _VALUE_3_OFFSET + instructions[1]
    mux_rite = _VALUE_4_OFFSET + instructions[2]
    if its_ok_to_move:
        write_serial_string(mux_left)
        write_serial_string(mux_rite)

def get_message_to_send(mux_X, mux_Y, left, right):
    f'{mux_X} {mux_Y} 0 0'

max_speed = 100 
multiply_by_3_limit = 5 
multiply_by_2_limit = 20 
multiply_by_1_limit = 100 

def getAdjustedValue(pos, mid):
    delta = pos - mid
    absDelta = abs(pos - mid)
    sign = delta / absDelta
    val = absDelta
    # val = min(2499, round(pow((delta/mid * 100), 2)))
    if absDelta < multiply_by_3_limit:
        val = absDelta * 3
    elif absDelta < multiply_by_2_limit:
        val = absDelta * 2
    val = min(100, val) * sign
    # val = min(600, round(pow((delta/mid * 100), 2)))
    # val = min(2499, round(pow((delta/mid * 100), 1)))
    return val * -1
    # return delta * -1

def write_serial_strings(valueA, valueB, valueC, valueD):
    try:
        ser.write(getEncoded('a', valueA))
        ser.write(getEncoded('b', valueB))
        ser.write(getEncoded('c', valueC))
        ser.write(getEncoded('d', valueD))
        
    except Exception as e: 
        print('error in write_serial_string', e)

def getEncoded(prefix, value):
    strValue = '<' + prefix + str(value) + '>'
    return strValue.encode(encoding = 'ascii', errors = 'strict')

def write_serial_string(stringToWrite):
    try:
        # print(stringToWrite.encode(encoding = 'ascii', errors = 'strict'))
        ser.write(('<' + str(stringToWrite) + '>').encode(encoding = 'ascii', errors = 'strict'))
        
    except Exception as e: 
        print('error in write_serial_string 2', e)

def read_serial():
    
    incommingBYTES = ser.inWaiting()
    # print('incomming BYTES 1')
    # print(incommingBYTES)
    inBytes = ser.read(incommingBYTES)
    # print(inBytes)

    # line = ser.readline()
    # print('from arduino -> ' + line)
