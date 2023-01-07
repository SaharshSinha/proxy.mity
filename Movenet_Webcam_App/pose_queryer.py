from math import sin, cos, radians, pi, atan2, degrees, dist
from body_points import BodyPoint, BodyPointColor, color_array
import cv2

___MOVE_FORWARD: int = 8
___MOVE_BAKWARD: int = 2
___MOVE_FORWARD_LEFT: int = 7
___MOVE_FORWARD_RITE: int = 9
___MOVE_BAKWARD_LEFT: int = 1
___MOVE_BAKWARD_RITE: int = 3
___LOOK_LEFT: int = 4
___LOOK_RITE: int = 6
___STOP: int = 5
___ARMED: int = 0

_X_ = 0
_Y_ = 1

_ELBOW_ANGLE_LEFT_ACTIVE = 315 - 20
_ELBOW_ANGLE_LEFT_SIGNAL = _ELBOW_ANGLE_LEFT_ACTIVE - 90

# _ELBOW_ANGLE_LEFT_SIGNAL = _ELBOW_ANGLE_LEFT_ACTIVE # + 45

_ELBOW_ANGLE_RITE_ACTIVE_FORE = 225 + 20
_ELBOW_ANGLE_RITE_SIGNAL_FORE = _ELBOW_ANGLE_RITE_ACTIVE_FORE - 90
_ELBOW_ANGLE_RITE_ACTIVE_BACK = 315+22.5
_ELBOW_ANGLE_RITE_SIGNAL_BACK = _ELBOW_ANGLE_RITE_ACTIVE_BACK - 90
# _ELBOW_ANGLE_RITE_SIGNAL = 90 - 45

_ACTIVE_ELBOW_ANGLE_ERROR = 15

_BODY_TILT_THRESHOLD = 0.15

_HEAD_TURN_THRESHOLD = 0.4
_HEAD_TURN_THRESHOLD_BUFFER = 0.1
_HEAD_TURN_THRESHOLD_PERCENT = 40
_HEAD_TURN_INDICATOR_LENGTH = 50


_frame_count = 0

class point_stabilizer:
    stabilization_length = 12
    points: list
    sum_total: int
    def get_point(self, point):
        self.sum_total += point
        self.points.append(point)
        if len(self.points) > self.stabilization_length:
            subtractor = self.points.pop()
            self.sum_total -= subtractor
        return round(self.sum_total /  len(self.points))

class measures:
    _left_uppr_arm_angle = 0
    _left_fore_arm_angle = 0
    _left_fore_arm_angle_rel_to_upper_arm = 0
    _rite_uppr_arm_angle = 0
    _rite_fore_arm_angle = 0
    _rite_fore_arm_angle_rel_to_upper_arm = 0
    _left_ear_distance_from_nose = 0
    _rite_ear_distance_from_nose = 0
    _distance_between_nose_and_ear_midpoint = 0
    _ear_midpoint = 0
    _distance_between_ears = 0 
    nose_from_ear_mid_percent = 0
    angle_between_nose_and_ear_mid = 0 

    fps = ''
    left_hand_active = False
    rite_hand_active_fore = False
    rite_hand_active_back = False
    head_turned_left = False
    head_turned_rite = False
    head_turned_above = False
    head_turned_false = False

measure = measures()

def relative_point_pos(body_point, d, theta) -> list[int]:
    theta_rad = pi/2 - radians(theta)
    return [round(body_point[_X_] + d*cos(theta_rad)), round(body_point[_Y_] + d*sin(theta_rad))]

def point_pos(x0, y0, d, theta):
    theta_rad = pi/2 - radians(theta)
    return x0 + d*cos(theta_rad), y0 + d*sin(theta_rad)


def get_action_for_pose_v2(pose_points) -> int:
    set_angles_and_distances(pose_points)
    
    measure.left_hand_active = left_hand_is_active(pose_points)
    # measure.rite_hand_active_fore = rite_hand_is_active_fore(pose_points)
    # measure.rite_hand_active_back = rite_hand_is_active_back(pose_points)
    measure.head_turned_left = head_is_turned_left(pose_points)
    measure.head_turned_rite = head_is_turned_rite(pose_points)
    measure.head_turned_above = head_is_turned_above(pose_points)
    measure.head_turned_below = head_is_turned_below(pose_points)

    # print('left_hand_active: ' + str(left_hand_active))
    # print('rite_hand_active_fore: ' + str(rite_hand_active_fore))
    # print('rite_hand_active_back: ' + str(rite_hand_active_back))
    # print('head_turned_left: ' + str(head_turned_left))
    # print('head_turned_rite: ' + str(head_turned_rite))


    signal = 5
    
    if   measure.left_hand_active and measure.rite_hand_active_fore and measure.head_turned_left:
        signal = ___MOVE_FORWARD_LEFT
    elif measure.left_hand_active and measure.rite_hand_active_fore and measure.head_turned_rite:
        signal = ___MOVE_FORWARD_RITE
    elif measure.left_hand_active and measure.rite_hand_active_fore:
        signal = ___MOVE_FORWARD

    elif measure.left_hand_active and measure.rite_hand_active_back and measure.head_turned_left:
        signal = ___MOVE_BAKWARD_LEFT
    elif measure.left_hand_active and measure.rite_hand_active_back and measure.head_turned_rite:
        signal = ___MOVE_BAKWARD_RITE
    elif measure.left_hand_active and measure.rite_hand_active_back:
        signal = ___MOVE_BAKWARD
        
    elif measure.left_hand_active and measure.head_turned_left:
        signal = ___LOOK_LEFT
    elif measure.left_hand_active and measure.head_turned_rite:
        signal = ___LOOK_RITE
        
    return signal
    
def head_is_turned_left(pose_points) -> bool:
    """

    :rtype: bool
    """
    rite_ear_min_distance = measure._rite_ear_distance_from_nose * (_HEAD_TURN_THRESHOLD - _HEAD_TURN_THRESHOLD_BUFFER)
    rite_ear_max_distance = measure._rite_ear_distance_from_nose * (_HEAD_TURN_THRESHOLD + (_HEAD_TURN_THRESHOLD_BUFFER * 3))
    return (
        rite_ear_min_distance <= measure._left_ear_distance_from_nose and 
        measure._left_ear_distance_from_nose <= rite_ear_max_distance)


def head_is_turned_rite(pose_points) -> bool:
    """

    :rtype: bool
    """
    left_ear_min_distance = measure._left_ear_distance_from_nose * (_HEAD_TURN_THRESHOLD - _HEAD_TURN_THRESHOLD_BUFFER)
    left_ear_max_distance = measure._left_ear_distance_from_nose * (_HEAD_TURN_THRESHOLD + (_HEAD_TURN_THRESHOLD_BUFFER*3))
    return (
        left_ear_min_distance <= measure._rite_ear_distance_from_nose and 
        measure._rite_ear_distance_from_nose <= left_ear_max_distance)

def head_is_turned_vertically(pose_points):
    
    if measure._distance_between_nose_and_ear_midpoint > (measure._distance_between_ears / 2):
        if measure._ear_midpoint[_Y_] < pose_points[BodyPoint.nose.value][_Y_]:
            return 1
        else:
            return -1
    else:
        return 0

def head_is_turned_above(pose_points) -> bool:
    """

    :rtype: bool
    """
    if head_is_turned_vertically(pose_points) == 1:
        return True
    else:
        return False

def head_is_turned_below(pose_points) -> bool:
    """

    :rtype: bool
    """
    if head_is_turned_vertically(pose_points) == -1:
        return True
    else:
        return False


def left_hand_is_active(pose_points) -> bool:
    """

    :rtype: bool
    """
    left_elbow_angle = get_angle_elbow_left(pose_points)
    # print ('left_elbow_angle: ', str(left_elbow_angle))
    return (
            left_elbow_angle >= (_ELBOW_ANGLE_LEFT_SIGNAL - _ACTIVE_ELBOW_ANGLE_ERROR) and
            left_elbow_angle <= (_ELBOW_ANGLE_LEFT_SIGNAL + _ACTIVE_ELBOW_ANGLE_ERROR))


def rite_hand_is_active_fore(pose_points) -> bool:
    """

    :rtype: bool
    """
    rite_elbow_angle = get_angle_elbow_rite(pose_points)
    return (
            rite_elbow_angle >= (_ELBOW_ANGLE_RITE_SIGNAL_FORE - _ACTIVE_ELBOW_ANGLE_ERROR) and
            rite_elbow_angle <= (_ELBOW_ANGLE_RITE_SIGNAL_FORE + _ACTIVE_ELBOW_ANGLE_ERROR))


def rite_hand_is_active_back(pose_points) -> bool:
    """

    :rtype: bool
    """
    rite_elbow_angle = get_angle_elbow_rite(pose_points)
    return (
            rite_elbow_angle >= (_ELBOW_ANGLE_RITE_SIGNAL_BACK - _ACTIVE_ELBOW_ANGLE_ERROR) and
            rite_elbow_angle <= (_ELBOW_ANGLE_RITE_SIGNAL_BACK + _ACTIVE_ELBOW_ANGLE_ERROR))


def get_distance_ear_left_from_nose(pose_points) -> float:
    """

    :rtype: float
    """
    return get_distance_between_points_normalized(
        pose_points,
        BodyPoint.ear_left,
        BodyPoint.nose,
        BodyPoint.ear_left,
        BodyPoint.ear_rite)


def get_distance_ear_rite_from_nose(pose_points) -> float:
    """

    :rtype: float
    """
    return get_distance_between_points_normalized(
        pose_points,
        BodyPoint.ear_rite,
        BodyPoint.nose,
        BodyPoint.ear_left,
        BodyPoint.ear_rite)


def get_angle_elbow_left(pose_points) -> float:
    """

    :rtype: float
    """
    measure._left_fore_arm_angle_rel_to_upper_arm = (
        # 360 - 
        measure._left_fore_arm_angle -
        measure._left_uppr_arm_angle
    )
    return measure._left_fore_arm_angle_rel_to_upper_arm

def get_angle_elbow_rite(pose_points) -> float:
    """

    :rtype: float
    """
    measure._rite_fore_arm_angle_rel_to_upper_arm =  (
        measure._rite_fore_arm_angle -
        measure._rite_uppr_arm_angle
    )
    return measure._rite_fore_arm_angle_rel_to_upper_arm


def get_distance_between_points_normalized(pose_points, a: BodyPoint, bx: BodyPoint, by1: BodyPoint, by2: BodyPoint) -> float:
    """
    no one what this method does. That's why commenting should not be procastinated
    :rtype: float
    """
    body_point_a = pose_points[a.value]
    body_point_bx = pose_points[bx.value]
    body_point_by1 = pose_points[by1.value]
    body_point_by2 = pose_points[by2.value]
    normalized_body_point = [ body_point_bx[_X_], (body_point_by1[_Y_] + body_point_by2[_Y_]) / 2]
    # print ('            body_point_a: ', body_point_a)
    # print ('            body_point_bx: ', body_point_bx)
    # print ('            body_point_by1: ', body_point_by1)
    # print ('            body_point_by2: ', body_point_by2)
    # print ('            normalized_body_point: ', normalized_body_point)
    return get_distance(body_point_a, normalized_body_point)

def set_angles_and_distances(pose_points):
    measure._left_uppr_arm_angle = get_angle_absolute(pose_points[BodyPoint.elbow_left.value], pose_points[BodyPoint.shoulder_left.value])
    measure._left_fore_arm_angle = get_angle_absolute(pose_points[BodyPoint.elbow_left.value], pose_points[BodyPoint.   wrist_left.value])
    measure._rite_uppr_arm_angle = get_angle_absolute(pose_points[BodyPoint.elbow_rite.value], pose_points[BodyPoint.shoulder_rite.value])
    measure._rite_fore_arm_angle = get_angle_absolute(pose_points[BodyPoint.elbow_rite.value], pose_points[BodyPoint.   wrist_rite.value])
    measure._left_ear_distance_from_nose = get_distance_ear_left_from_nose(pose_points)
    measure._rite_ear_distance_from_nose = get_distance_ear_rite_from_nose(pose_points)

    measure._ear_midpoint = get_mid_point(pose_points, BodyPoint.ear_left, BodyPoint.ear_rite)
    measure._distance_between_ears = get_distance_between_body_points(pose_points, BodyPoint.ear_left, BodyPoint.ear_rite)
    measure._distance_between_nose_and_ear_midpoint = get_distance(measure._ear_midpoint, pose_points[BodyPoint.nose.value])
    measure.nose_from_ear_mid_percent = measure._distance_between_nose_and_ear_midpoint / measure._distance_between_ears * 100
    measure.angle_between_nose_and_ear_mid = get_angle(
        (0, measure._ear_midpoint[_Y_]),
        measure._ear_midpoint,
        pose_points[BodyPoint.nose.value]
    )

def get_angle_between_points(pose_points, a: BodyPoint, b: BodyPoint, c: BodyPoint) -> float:
    """

    :rtype: float
    """
    body_point_a = pose_points[a.value]
    body_point_b = pose_points[b.value]
    body_point_c = pose_points[c.value]
    return get_angle(body_point_a, body_point_b, body_point_c)

def get_distance_between_body_points(pose_points, p1: BodyPoint, p2: BodyPoint):
    return get_distance(pose_points[p1.value], pose_points[p2.value])

def get_mid_point(pose_points, p1: BodyPoint, p2: BodyPoint):
    return (
        round((pose_points[p1.value][_X_] + pose_points[p2.value][_X_])/2),
        round((pose_points[p1.value][_Y_] + pose_points[p2.value][_Y_])/2))

def get_distance(a, b) -> float:
    """

    :rtype: float
    """
    return dist(a, b)

def get_angle_absolute(a, b) -> float:
    """

    :rtype: float
    """
    return get_angle([0, a[_Y_]], a, b)


def get_angle(a, b, c) -> float:
    """

    :rtype: float
    """
    ang = degrees(atan2(c[_Y_]-b[_Y_], c[_X_]-b[_X_]) - atan2(a[_Y_]-b[_Y_], a[_X_]-b[_X_]))
    return ang + 360 if ang < 0 else ang
