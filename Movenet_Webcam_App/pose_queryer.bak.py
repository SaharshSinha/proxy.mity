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

_ELBOW_ANGLE_LEFT_ACTIVE = 225
_ELBOW_ANGLE_LEFT_SIGNAL = _ELBOW_ANGLE_LEFT_ACTIVE # + 45

_ELBOW_ANGLE_RITE_ACTIVE = 90
_ELBOW_ANGLE_RITE_SIGNAL = 90 - 45

_ACTIVE_ELBOW_ANGLE_ERROR = 15

_BODY_TILT_THRESHOLD = 0.15

_HEAD_TURN_THRESHOLD = 0.4
_HEAD_TURN_THRESHOLD_BUFFER = 0.1
_HEAD_TURN_THRESHOLD_PERCENT = 40
_HEAD_TURN_INDICATOR_LENGTH = 50

_FOREARM_OVERLAY_WHITE = cv2.imread('images/triangle.png', -1)
_POINT_OVERLAY_WHITE_LEFT = cv2.imread('images/point.png', -1)
_ROTATOR = cv2.imread('images/rotator.png', -1)

_FORWARD = cv2.imread('images/forward.56.png', -1)
_FORWARD_LEFT = cv2.imread('images/forward-left.56.png', -1)
_FORWARD_RITE = cv2.imread('images/forward-rite.56.png', -1)

_BACKWARD = cv2.imread('images/backward.56.png', -1)
_BACKWARD_LEFT = cv2.imread('images/backward-left.56.png', -1)
_BACKWARD_RITE = cv2.imread('images/backward-rite.56.png', -1)

_TURN_LEFT = cv2.imread('images/turn-left.56.png', -1)
_TURN_RITE = cv2.imread('images/turn-rite.56.png', -1)

_NO_GO = cv2.imread('images/no-go.56.png', -1)

signal_image_map = {
    ___MOVE_FORWARD: _FORWARD,
    ___MOVE_BAKWARD: _BACKWARD,
    ___MOVE_FORWARD_LEFT: _FORWARD_LEFT,
    ___MOVE_FORWARD_RITE: _FORWARD_RITE,
    ___MOVE_BAKWARD_LEFT: _BACKWARD_LEFT,
    ___MOVE_BAKWARD_RITE: _BACKWARD_RITE,
    ___LOOK_LEFT: _TURN_LEFT,
    ___LOOK_RITE: _TURN_RITE,
    ___STOP: _NO_GO,
    ___ARMED: _NO_GO,
}

_frame_count = 0


tracking_points = set([
    BodyPoint.ear_left.value,
    BodyPoint.ear_rite.value,
    BodyPoint.shoulder_left.value,
    BodyPoint.shoulder_rite.value,
    BodyPoint.elbow_left.value,
    BodyPoint.elbow_rite.value,
    BodyPoint.wrist_left.value,
    BodyPoint.wrist_rite.value])

print (tracking_points)


def relative_point_pos(body_point, d, theta) -> list[int]:
    theta_rad = pi/2 - radians(theta)
    return [round(body_point[_X_] + d*cos(theta_rad)), round(body_point[_Y_] + d*sin(theta_rad))]

def point_pos(x0, y0, d, theta):
    theta_rad = pi/2 - radians(theta)
    return x0 + d*cos(theta_rad), y0 + d*sin(theta_rad)

def show_points(img, idx: int, xc: int, yc: int):
    point_color = (0, 0, 0)
    radius = 2
    thickness = 1
    # print(idx)
    if idx in tracking_points:
        point_color = color_array[idx]
        radius = 6
        thickness = 4

    if idx % 2 == 1:
        img = cv2.circle(img, (xc, yc), radius, point_color, thickness)
    else:
        img = cv2.rectangle(
            img, 
            (int(xc - radius), int(yc - radius)), 
            (int(xc + radius), int(yc + radius)), 
            point_color,
            thickness)
    return img

def show_points_v2(img, frame_idx: int, point_idx: int, xc: int, yc: int):
    if point_idx == frame_idx % 4:
        return place_image(img, _POINT_OVERLAY_WHITE_LEFT, (xc, yc), 0, 1, 1)
    return img

def place_image(background, overlay, center_position, angle = 0, size = 1, opacity = 1):
    if opacity == 0 or size == 0:
        return 
        
    x_offset = center_position[0] - int(overlay.shape[1] / 2)
    y_offset = center_position[1] - int(overlay.shape[0] / 2)

    x_min = x_offset 
    x_max = x_offset + overlay.shape[1]
    y_min = y_offset
    y_max = y_offset + overlay.shape[0]

    if x_max < 0 or y_max < 0 or x_min > background.shape[1] or y_min > background.shape[0]:
        return 
    
    x_background_min = max(0, x_min) 
    x_background_max = min(background.shape[1], x_max)
    y_background_min = max(0, y_min)
    y_background_max = min(background.shape[0], y_max)
    
    x_min_delta = abs(x_background_min - x_min)
    y_min_delta = abs(y_background_min - y_min)
    x_max_delta = abs(x_background_max - x_max)
    y_max_delta = abs(y_background_max - y_max)

    x_overlay_min = x_min_delta 
    x_overlay_max = overlay.shape[1] - x_max_delta
    y_overlay_min = y_min_delta 
    y_overlay_max = overlay.shape[0] - y_max_delta

    height, width = overlay.shape[:2]
    center = (width/2, height/2)

    if angle != 0 or size != 1:
        rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=angle, scale=1)
        overlay  = cv2.warpAffine(src=overlay, M=rotate_matrix, dsize=(width, height))

    alpha_s = overlay[y_overlay_min:y_overlay_max, x_overlay_min:x_overlay_max, 3] / 255.0 * opacity
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        background[y_background_min:y_background_max, x_background_min:x_background_max, c] = (
            alpha_s * overlay[y_overlay_min:y_overlay_max, x_overlay_min:x_overlay_max, c] + 
            alpha_l * background[y_background_min:y_background_max, x_background_min:x_background_max, c])

    return background


def get_action_for_pose_v2(pose_points) -> int:
    left_hand_active = left_hand_is_active(pose_points)
    rite_hand_active_fore = rite_hand_is_active_fore(pose_points)
    rite_hand_active_back = rite_hand_is_active_back(pose_points)
    head_turned_left = head_is_turned_left(pose_points)
    head_turned_rite = head_is_turned_rite(pose_points)

    signal = 5
    
    if   left_hand_active and rite_hand_active_fore and head_turned_left:
        signal = ___MOVE_FORWARD_LEFT
    elif left_hand_active and rite_hand_active_fore and head_turned_rite:
        signal = ___MOVE_FORWARD_RITE
    elif left_hand_active and rite_hand_active_fore:
        signal = ___MOVE_FORWARD

    elif left_hand_active and rite_hand_active_back and head_turned_left:
        signal = ___MOVE_BAKWARD_LEFT
    elif left_hand_active and rite_hand_active_back and head_turned_rite:
        signal = ___MOVE_BAKWARD_RITE
    elif left_hand_active and rite_hand_active_back:
        signal = ___MOVE_BAKWARD
        
    elif left_hand_active and head_turned_left:
        signal = ___LOOK_LEFT
    elif left_hand_active and head_turned_rite:
        signal = ___LOOK_RITE
        
    return signal
    
def draw_visual_cues_v2(pose_points: list, img: any, width: int, height: int) -> any:
    left_elbow_point = pose_points[BodyPoint.elbow_left.value]
    rite_elbow_point = pose_points[BodyPoint.elbow_rite.value]

    left_shoulder_point = pose_points[BodyPoint.shoulder_left.value]
    rite_shoulder_point = pose_points[BodyPoint.shoulder_rite.value]

    left_elbow_plane_point = (0, left_elbow_point[_Y_])
    rite_elbow_plane_point = (0, rite_elbow_point[_Y_])
    
    left_upper_arm_angle = get_angle(left_elbow_plane_point, left_elbow_point, left_shoulder_point)
    rite_upper_arm_angle = get_angle(rite_elbow_plane_point, rite_elbow_point, rite_shoulder_point)

    # left_elbow_angle = get_angle_elbow_left(pose_points)
    # rite_elbow_angle = get_angle_elbow_rite(pose_points)

    left_elbow_absolute_angle = -1 * ((left_upper_arm_angle + _ELBOW_ANGLE_LEFT_ACTIVE) % 360)
    rite_elbow_absolute_angle = -1 * ((rite_upper_arm_angle + _ELBOW_ANGLE_RITE_ACTIVE) % 360)
    
    motion_image = signal_image_map[get_action_for_pose_v2(pose_points=pose_points)]
    print (motion_image)
    img = place_image(img, _FOREARM_OVERLAY_WHITE, left_elbow_point, left_elbow_absolute_angle, 1, 1)
    img = place_image(img, motion_image, (int(width/2), int(height/2)))
    # img = place_image(img, _ROTATOR, (width/2, 10), 0, 1, 1)

    return img

def draw_visual_cues_v1(pose_points: list, img: any, width: int, height: int) -> any:
    midpoint_x = int(width / 2)
    
    nose_point = pose_points[BodyPoint.nose.value]
    
    eye_left_point = pose_points[BodyPoint.eye_left.value]
    eye_rite_point = pose_points[BodyPoint.eye_rite.value]
    
    ear_left_point = pose_points[BodyPoint.ear_left.value]
    ear_rite_point = pose_points[BodyPoint.ear_rite.value]
    
    shoulder_left_point = pose_points[BodyPoint.shoulder_left.value]
    shoulder_rite_point = pose_points[BodyPoint.shoulder_rite.value]
    
    waist_left_point = pose_points[BodyPoint.waist_left.value]
    waist_rite_point = pose_points[BodyPoint.waist_rite.value]

    ear_distance_left = get_distance(ear_left_point, nose_point)
    ear_distance_rite = get_distance(ear_rite_point, nose_point)


    shoulder_distance: float = get_distance_between_shoulders(pose_points)
    shoulder_height = (shoulder_distance * _BODY_TILT_THRESHOLD)
    shoulder_height_adjustment =  int((shoulder_height - abs(shoulder_left_point[_Y_] - shoulder_rite_point[_Y_]))/2)


    percent_write_point_from = (midpoint_x, 20)
    percent_write_point_full_left = (midpoint_x + _HEAD_TURN_INDICATOR_LENGTH, 30)
    percent_write_point_full_rite = (midpoint_x - _HEAD_TURN_INDICATOR_LENGTH, 30)

    if ear_distance_left < ear_distance_rite:
        actual_percent_length = int((100 / _HEAD_TURN_THRESHOLD_PERCENT) * (_HEAD_TURN_INDICATOR_LENGTH - int(ear_distance_left / ear_distance_rite * 100))) 
        percent_write_point_real = (midpoint_x + actual_percent_length, 30)
    elif ear_distance_left > ear_distance_rite:
        actual_percent_length = int((100 / _HEAD_TURN_THRESHOLD_PERCENT) * (_HEAD_TURN_INDICATOR_LENGTH - int(ear_distance_rite / ear_distance_left * 100))) 
        percent_write_point_real = (midpoint_x - actual_percent_length, 30)
    else:
        percent_write_point_from = (0,0)
        percent_write_point_real = (0,0)

    img = cv2.rectangle(img, percent_write_point_from, percent_write_point_real, BodyPointColor.nose.value, -1)

    img = cv2.rectangle(img, percent_write_point_from, percent_write_point_full_left, (0,0,0), 1)
    img = cv2.rectangle(img, percent_write_point_from, percent_write_point_full_rite, (0,0,0), 1)
    
    # img = cv2.putText(
    #     img, 
    #     str(percent_length), 
    #     percent_write_point, 
    #     cv2.FONT_HERSHEY_SIMPLEX,
    #     1, 
    #     (0,0,0), 
    #     1, 
    #     cv2.LINE_AA)
    
    nose_x = nose_point[_X_]
    cue_body_left_x = nose_x - 10
    cue_body_rite_x = nose_x + 10

    left_elbow_point = pose_points[BodyPoint.elbow_left.value]
    rite_elbow_point = pose_points[BodyPoint.elbow_rite.value]

    left_shoulder_point = pose_points[BodyPoint.shoulder_left.value]
    rite_shoulder_point = pose_points[BodyPoint.shoulder_rite.value]

    left_elbow_plane_point = (0, left_elbow_point[_Y_])
    rite_elbow_plane_point = (0, rite_elbow_point[_Y_])
    
    left_upper_arm_angle = get_angle(left_elbow_plane_point, left_elbow_point, left_shoulder_point)
    rite_upper_arm_angle = get_angle(rite_elbow_plane_point, rite_elbow_point, rite_shoulder_point)

    left_elbow_angle = get_angle_elbow_left(pose_points)
    rite_elbow_angle = get_angle_elbow_rite(pose_points)

    left_elbow_absolute_angle = -1 * ((left_upper_arm_angle + _ELBOW_ANGLE_LEFT_ACTIVE) % 360)
    rite_elbow_absolute_angle = -1 * ((rite_upper_arm_angle + _ELBOW_ANGLE_RITE_ACTIVE) % 360)
    
    left_arm_point_max = relative_point_pos(
        left_elbow_point, 
        3 * get_distance(
            pose_points[BodyPoint.elbow_left.value], 
            pose_points[BodyPoint.wrist_left.value]),
        left_elbow_absolute_angle + _ACTIVE_ELBOW_ANGLE_ERROR)
    
    left_arm_angle_min = relative_point_pos(
        left_elbow_point, 
        3 * get_distance(
            pose_points[BodyPoint.elbow_left.value], 
            pose_points[BodyPoint.wrist_left.value]),
        left_elbow_absolute_angle - _ACTIVE_ELBOW_ANGLE_ERROR)
    
    # print(left_elbow_point)
    # print(left_arm_point_max)

    img = cv2.line(img, 
        (left_elbow_point[_X_], left_elbow_point[_Y_]), 
        (left_arm_point_max[_X_], left_arm_point_max[_Y_]), 
        BodyPointColor.ear_left.value,
        2 )
    
    img = cv2.line(img, 
        (left_elbow_point[_X_], left_elbow_point[_Y_]), 
        (left_arm_angle_min[_X_], left_arm_angle_min[_Y_]), 
        BodyPointColor.ear_left.value,
        2 )

    img = cv2.putText(img, 
        str(round(left_elbow_angle)) + '; ' + str(round(left_upper_arm_angle)) + '; ' + str(round(left_elbow_absolute_angle)), 
        left_elbow_point, 
        cv2.FONT_HERSHEY_SIMPLEX, 
        1, 
        (200, 200, 200), 
        2, 
        cv2.LINE_AA)
    
    img = cv2.putText(img, 
        str(round(rite_elbow_angle)), 
        rite_elbow_point, 
        cv2.FONT_HERSHEY_SIMPLEX, 
        1, 
        (200, 200, 200), 
        2, 
        cv2.LINE_AA)

    # img = cv2.line(img, 
    #     (cue_body_left_x, shoulder_left_point[_Y_]), 
    #     (cue_body_left_x, waist_left_point[_Y_]), 
    #     BodyPointColor.ear_left.value,
    #     2 )
        
    # img = cv2.line(img, 
    #     (cue_body_rite_x, shoulder_rite_point[_Y_]), 
    #     (cue_body_rite_x, waist_rite_point[_Y_]), 
    #     BodyPointColor.ear_rite.value,
    #     2 )

    shoulder_distance_offset = round((shoulder_left_point[_X_] - shoulder_rite_point[_X_]) / 3)

    img = cv2.rectangle(img,
        (shoulder_left_point[_X_] + shoulder_distance_offset, shoulder_left_point[_Y_]),
        (shoulder_rite_point[_X_] - shoulder_distance_offset, shoulder_rite_point[_Y_]),
        BodyPointColor.nose.value,
        -1)


    img = cv2.rectangle(img,
        (shoulder_left_point[_X_], min(shoulder_left_point[_Y_], shoulder_rite_point[_Y_]) - shoulder_height_adjustment),
        (shoulder_rite_point[_X_], max(shoulder_left_point[_Y_], shoulder_rite_point[_Y_]) + shoulder_height_adjustment),
        BodyPointColor.waist_left.value,
        1)

    # cue_body_left = [ [cue_body_left_x, shoulder_left_point[_Y_]], [cue_body_left_x, waist_left_point[_Y_]] ]
    # cue_body_rite = [ [cue_body_rite_x, shoulder_rite_point[_Y_]], [cue_body_rite_x, waist_rite_point[_Y_]] ]

    return img

def overlay(img, overlay_img, angle = 0, scale = 1):

    img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
    overlay_img = cv2.cvtColor(overlay_img, cv2.COLOR_RGB2RGBA)
    height, width = (img.shape[0] , img.shape[1])
    size = (width, height)
    center = (width/2,height/2)
    
    rotation_matrix = cv2.getRotationMatrix2D(
        center, 
        angle, 
        scale)

    overlay_img_dst = cv2.warpAffine(
        overlay_img, 
        rotation_matrix, 
        size,
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_TRANSPARENT)

    x_offset = int((img.shape[1] - overlay_img_dst.shape[1])/2)
    y_offset =  int((img.shape[0] - overlay_img_dst.shape[0])/2)

    y1, y2 = y_offset, y_offset + overlay_img_dst.shape[0]
    x1, x2 = x_offset, x_offset + overlay_img_dst.shape[1]

    alpha_s = overlay_img_dst[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        img[y1:y2, x1:x2, c] = (alpha_s * overlay_img_dst[:, :, c] + alpha_l * img[y1:y2, x1:x2, c])

    return img

def get_vertical_line(point) -> list:
    return [ point, [ point[_X_], point[_Y_] - 20]]

def get_action_for_pose(pose_points) -> int:
    if left_hand_is_active(pose_points):
        if False:
            return 5
        elif head_is_turned_left(pose_points):
            return ___LOOK_LEFT
        elif head_is_turned_rite(pose_points):
            return ___LOOK_RITE
        elif body_is_tilted_left(pose_points):
            return ___MOVE_FORWARD_LEFT
        elif body_is_tilted_rite(pose_points):
            return ___MOVE_FORWARD_RITE
        elif rite_hand_is_signalling(pose_points):
            return ___MOVE_FORWARD
        else:
            return ___STOP
    elif rite_hand_is_active(pose_points):
        if False:
            return 5
        elif head_is_turned_left(pose_points):
            return ___LOOK_LEFT
        elif head_is_turned_rite(pose_points):
            return ___LOOK_RITE
        elif body_is_tilted_left(pose_points):
            return ___MOVE_BAKWARD_LEFT
        elif body_is_tilted_rite(pose_points):
            return ___MOVE_BAKWARD_RITE
        elif left_hand_is_signalling(pose_points):
            return ___MOVE_BAKWARD
        else:
            return ___STOP
    else:
        return ___STOP


def head_is_turned_left(pose_points) -> bool:
    """

    :rtype: bool
    """
    left_ear_distance: float = get_distance_ear_left_from_nose(pose_points)
    rite_ear_distance: float = get_distance_ear_rite_from_nose(pose_points)
    rite_ear_min_distance = rite_ear_distance * (_HEAD_TURN_THRESHOLD - _HEAD_TURN_THRESHOLD_BUFFER)
    rite_ear_max_distance = rite_ear_distance * (_HEAD_TURN_THRESHOLD + (_HEAD_TURN_THRESHOLD_BUFFER * 3))
    # print ('    left_ear_distance: ', str(left_ear_distance))
    # print ('    rite_ear_distance: ', str(rite_ear_distance))
    # print ('    rite_ear_min_distance: ', str(rite_ear_min_distance))
    # print ('    rite_ear_max_distance: ', str(rite_ear_max_distance))
    # print ('    -----')
    return (rite_ear_min_distance <= left_ear_distance and left_ear_distance <= rite_ear_max_distance)


def head_is_turned_rite(pose_points) -> bool:
    """

    :rtype: bool
    """
    left_ear_distance: float = get_distance_ear_left_from_nose(pose_points)
    rite_ear_distance: float = get_distance_ear_rite_from_nose(pose_points)
    left_ear_min_distance = left_ear_distance * (_HEAD_TURN_THRESHOLD - _HEAD_TURN_THRESHOLD_BUFFER)
    left_ear_max_distance = left_ear_distance * (_HEAD_TURN_THRESHOLD + (_HEAD_TURN_THRESHOLD_BUFFER*3))
    # print ('    rite_ear_distance: ', str(rite_ear_distance))
    # print ('    left_ear_distance: ', str(left_ear_distance))
    # print ('    left_ear_min_distance: ', str(left_ear_min_distance))
    # print ('    left_ear_max_distance: ', str(left_ear_max_distance))
    # print ('    -----')
    return (left_ear_min_distance <= rite_ear_distance and rite_ear_distance <= left_ear_max_distance)


def body_is_tilted_left(pose_points) -> bool:
    """

    :rtype: bool
    """
    shoulder_distance: float = get_distance_between_shoulders(pose_points)
    shoulder_height_difference = get_diffrence_between_shoulder_heights(pose_points)
    # print ('        shoulder_distance: ', str(shoulder_distance))
    # print ('        shoulder_height_difference: ', str(shoulder_height_difference))
    # print ('        -----')
    return (shoulder_height_difference >= (shoulder_distance * _BODY_TILT_THRESHOLD))


def body_is_tilted_rite(pose_points) -> bool:
    """

    :rtype: bool
    """
    shoulder_distance: float = get_distance_between_shoulders(pose_points)
    shoulder_height_difference = get_diffrence_between_shoulder_heights(pose_points) * -1
    # print ('        shoulder_distance: ', str(shoulder_distance))
    # print ('        shoulder_height_difference: ', str(shoulder_height_difference))
    # print ('        -----')
    return (shoulder_height_difference >= (shoulder_distance * _BODY_TILT_THRESHOLD))


def left_hand_is_active(pose_points) -> bool:
    """

    :rtype: bool
    """
    left_elbow_angle = get_angle_elbow_left(pose_points)
    # print ('left_elbow_angle: ', str(left_elbow_angle))
    return (
            left_elbow_angle >= (_ELBOW_ANGLE_LEFT_ACTIVE - _ACTIVE_ELBOW_ANGLE_ERROR) and
            left_elbow_angle <= (_ELBOW_ANGLE_LEFT_ACTIVE + _ACTIVE_ELBOW_ANGLE_ERROR))


def rite_hand_is_active_fore(pose_points) -> bool:
    """

    :rtype: bool
    """
    rite_elbow_angle = get_angle_elbow_left(pose_points)
    # print ('rite_elbow_angle: ', str(rite_elbow_angle))
    return (
            rite_elbow_angle >= (_ELBOW_ANGLE_RITE_ACTIVE - _ACTIVE_ELBOW_ANGLE_ERROR) and
            rite_elbow_angle <= (_ELBOW_ANGLE_RITE_ACTIVE + _ACTIVE_ELBOW_ANGLE_ERROR))


def rite_hand_is_active_back(pose_points) -> bool:
    """

    :rtype: bool
    """
    rite_elbow_angle = get_angle_elbow_left(pose_points)
    # print ('rite_elbow_angle: ', str(rite_elbow_angle))
    return (
            rite_elbow_angle >= (_ELBOW_ANGLE_RITE_ACTIVE - _ACTIVE_ELBOW_ANGLE_ERROR) and
            rite_elbow_angle <= (_ELBOW_ANGLE_RITE_ACTIVE + _ACTIVE_ELBOW_ANGLE_ERROR))



def left_hand_is_signalling(pose_points) -> bool:
    """

    :rtype: bool
    """
    left_elbow_angle = get_angle_elbow_left(pose_points)
    # print ('left_elbow_angle: ', str(left_elbow_angle))
    return (
            left_elbow_angle >= (_ELBOW_ANGLE_LEFT_SIGNAL - _ACTIVE_ELBOW_ANGLE_ERROR) and
            left_elbow_angle <= (_ELBOW_ANGLE_LEFT_SIGNAL + _ACTIVE_ELBOW_ANGLE_ERROR))



def rite_hand_is_active(pose_points) -> bool:
    """

    :rtype: bool
    """
    rite_elbow_angle = get_angle_elbow_rite(pose_points)
    # print ('rite_elbow_angle: ', str(rite_elbow_angle))
    return (
            rite_elbow_angle >= (_ELBOW_ANGLE_RITE_ACTIVE - _ACTIVE_ELBOW_ANGLE_ERROR) and
            rite_elbow_angle <= (_ELBOW_ANGLE_RITE_ACTIVE + _ACTIVE_ELBOW_ANGLE_ERROR))


def rite_hand_is_signalling(pose_points) -> bool:
    """

    :rtype: bool
    """
    rite_elbow_angle = get_angle_elbow_rite(pose_points)
    # print ('    rite_elbow_angle: ', str(rite_elbow_angle))
    # print ('    -----')
    return (
            rite_elbow_angle >= (_ELBOW_ANGLE_RITE_SIGNAL - _ACTIVE_ELBOW_ANGLE_ERROR) and
            rite_elbow_angle <= (_ELBOW_ANGLE_RITE_SIGNAL + _ACTIVE_ELBOW_ANGLE_ERROR))


# def rite_hand_is_active_bakward(pose_points) -> bool:
#     """

#     :rtype: bool
#     """
#     rite_elbow_angle = get_angle_elbow_rite(pose_points)
#     return (
#             rite_elbow_angle >= (_ELBOW_ANGLE_RITE_SIGNAL - _ACTIVE_ELBOW_ANGLE_ERROR) and
#             rite_elbow_angle <= (_ELBOW_ANGLE_RITE_SIGNAL + _ACTIVE_ELBOW_ANGLE_ERROR))


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


# def get_distance_shoulder_left_from_nose(pose_points) -> float:
#     """

#     :rtype: float
#     """
#     return get_distance_between_points_normalized(
#         pose_points,
#         BodyPoint.shoulder_left,
#         BodyPoint.nose,
#         BodyPoint.shoulder_left,
#         BodyPoint.shoulder_rite)


# def get_distance_shoulder_rite_from_nose(pose_points) -> float:
#     """

#     :rtype: float
#     """
#     return get_distance_between_points_normalized(
#         pose_points,
#         BodyPoint.shoulder_rite,
#         BodyPoint.nose,
#         BodyPoint.shoulder_left,
#         BodyPoint.shoulder_rite)



# def get_distance_between_shoulders(pose_points) -> float:
    """

    :rtype: float
    """
    return get_distance_between_points(
        pose_points,
        BodyPoint.shoulder_left,
        BodyPoint.shoulder_rite)


# def get_diffrence_between_shoulder_heights(pose_points) -> float:
#     """

#     :rtype: float
#     """
#     return (pose_points[BodyPoint.shoulder_left.value][_Y_] - pose_points[BodyPoint.shoulder_rite.value][_Y_])


def get_angle_elbow_left(pose_points) -> float:
    """

    :rtype: float
    """
    return get_angle_between_points(
        pose_points,
        BodyPoint.shoulder_left,
        BodyPoint.elbow_left,
        BodyPoint.wrist_left)


def get_angle_elbow_rite(pose_points) -> float:
    """

    :rtype: float
    """
    return get_angle_between_points(
        pose_points,
        BodyPoint.shoulder_rite,
        BodyPoint.elbow_rite,
        BodyPoint.wrist_rite)


def get_distance_between_points(pose_points, a: BodyPoint, b: BodyPoint) -> float:
    """

    :rtype: float
    """
    body_point_a = pose_points[a.value]
    body_point_b = pose_points[b.value]
    return get_distance(body_point_a, body_point_b)


def get_distance_between_points_normalized(pose_points, a: BodyPoint, bx: BodyPoint, by1: BodyPoint, by2: BodyPoint) -> float:
    """

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


def get_angle_between_points(pose_points, a: BodyPoint, b: BodyPoint, c: BodyPoint) -> float:
    """

    :rtype: float
    """
    body_point_a = pose_points[a.value]
    body_point_b = pose_points[b.value]
    body_point_c = pose_points[c.value]
    return get_angle(body_point_a, body_point_b, body_point_c)


def get_distance(a, b) -> float:
    """

    :rtype: float
    """
    return dist(a, b)


def get_angle(a, b, c) -> float:
    """

    :rtype: float
    """
    ang = degrees(atan2(c[_Y_]-b[_Y_], c[_X_]-b[_X_]) - atan2(a[_Y_]-b[_Y_], a[_X_]-b[_X_]))
    return ang + 360 if ang < 0 else ang
