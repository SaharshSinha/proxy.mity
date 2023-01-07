
from math import sin, cos, radians, pi, atan2, degrees, dist
from body_points import BodyPoint, BodyPointColor, color_array
import cv2
import pose_queryer

_X_ = 0
_Y_ = 1


_FOREARM_OVERLAY_WHITE_ACTIVATE = cv2.imread('images/activate.40.png', -1)
_FOREARM_OVERLAY_WHITE_ACTIVATE_READY = cv2.imread('images/activate-ready.40.png', -1)
_FOREARM_OVERLAY_WHITE_ACTIVATE_ACTIVE = cv2.imread('images/activate-active.40.png', -1)

# _FOREARM_OVERLAY_WHITE_ACCELERATE = cv2.imread('images/accelerate.40.png', -1)
# _FOREARM_OVERLAY_WHITE_ACCELERATE_READY = cv2.imread('images/accelerate-ready.40.png', -1)
# _FOREARM_OVERLAY_WHITE_ACCELERATE_ACTIVE = cv2.imread('images/accelerate-active.40.png', -1)

# _FOREARM_OVERLAY_WHITE_REVERSE = cv2.imread('images/reverse.40.png', -1)
# _FOREARM_OVERLAY_WHITE_REVERSE_READY = cv2.imread('images/reverse-ready.40.png', -1)
# _FOREARM_OVERLAY_WHITE_REVERSE_ACTIVE = cv2.imread('images/reverse-active.40.png', -1)

# _ROTATOR = cv2.imread('images/rotator-radial.14.png', -1)
# _ROTATOR_READY = cv2.imread('images/rotator-radial-ready.14.png', -1)
# _ROTATOR_ACTIVE = cv2.imread('images/rotator-radial-active.14.png', -1)

# _ROTATOR = cv2.imread('images/pointers/pointer_1.png', -1)
# _ROTATOR_READY = cv2.imread('images/pointers/pointer_1.png', -1)
# _ROTATOR_ACTIVE = cv2.imread('images/pointers/pointer_1.png', -1)

_activate_overlay_map = {
    False: _FOREARM_OVERLAY_WHITE_ACTIVATE,
    True: _FOREARM_OVERLAY_WHITE_ACTIVATE_ACTIVE,
}

# _accelerate_overlay_map = {
#     '00': _FOREARM_OVERLAY_WHITE_ACCELERATE,
#     '01': _FOREARM_OVERLAY_WHITE_ACCELERATE_READY,
#     '10': _FOREARM_OVERLAY_WHITE_ACCELERATE,
#     '11': _FOREARM_OVERLAY_WHITE_ACCELERATE_ACTIVE,
# }

# _reverse_overlay_map = {
#     '00': _FOREARM_OVERLAY_WHITE_REVERSE,
#     '01': _FOREARM_OVERLAY_WHITE_REVERSE_READY,
#     '10': _FOREARM_OVERLAY_WHITE_REVERSE,
#     '11': _FOREARM_OVERLAY_WHITE_REVERSE_ACTIVE,
# }

# _rotator_overlay_map = {
#     '00': _ROTATOR,
#     '01': _ROTATOR_READY,
#     '10': _ROTATOR,
#     '11': _ROTATOR_ACTIVE,
# }


_POINT_OVERLAY_WHITE_LEFT = cv2.imread('images/point.png', -1)

_FORWARD = cv2.imread('images/forward.72.png', -1)
_FORWARD_LEFT = cv2.imread('images/forward-left.72.png', -1)
_FORWARD_RITE = cv2.imread('images/forward-rite.72.png', -1)

_BACKWARD = cv2.imread('images/backward.72.png', -1)
_BACKWARD_LEFT = cv2.imread('images/backward-left.72.png', -1)
_BACKWARD_RITE = cv2.imread('images/backward-rite.72.png', -1)

_TURN_LEFT = cv2.imread('images/turn-left.72.png', -1)
_TURN_RITE = cv2.imread('images/turn-rite.72.png', -1)

_NO_GO = cv2.imread('images/no-go.72.png', -1)

_INFONT_SIZE = 1
_INFONT_COLOR = 1
_INFONT_X = 1
_INFONT_Y = 1

pointer_images = [
    cv2.imread('images/pointers/pointer_1.png', -1),
    cv2.imread('images/pointers/pointer_2.png', -1),
    cv2.imread('images/pointers/pointer_3.png', -1),
    cv2.imread('images/pointers/pointer_4.png', -1),
    cv2.imread('images/pointers/pointer_5.png', -1),
    cv2.imread('images/pointers/pointer_6.png', -1),
    cv2.imread('images/pointers/pointer_7.png', -1),
    cv2.imread('images/pointers/pointer_8.png', -1),
    cv2.imread('images/pointers/pointer_9.png', -1),
    cv2.imread('images/pointers/pointer_10.png', -1),
    cv2.imread('images/pointers/pointer_11.png', -1),
    cv2.imread('images/pointers/pointer_12.png', -1),
    cv2.imread('images/pointers/pointer_13.png', -1),
    cv2.imread('images/pointers/pointer_14.png', -1)
]


signal_image_map = {
    pose_queryer.___MOVE_FORWARD: _FORWARD,
    pose_queryer.___MOVE_BAKWARD: _BACKWARD,
    pose_queryer.___MOVE_FORWARD_LEFT: _FORWARD_LEFT,
    pose_queryer.___MOVE_FORWARD_RITE: _FORWARD_RITE,
    pose_queryer.___MOVE_BAKWARD_LEFT: _BACKWARD_LEFT,
    pose_queryer.___MOVE_BAKWARD_RITE: _BACKWARD_RITE,
    pose_queryer.___LOOK_LEFT: _TURN_LEFT,
    pose_queryer.___LOOK_RITE: _TURN_RITE,
    pose_queryer.___STOP: _NO_GO,
    pose_queryer.___ARMED: _NO_GO,
}

# rotator_image_map = {
#     pose_queryer.___MOVE_FORWARD: _ROTATOR,
#     pose_queryer.___MOVE_BAKWARD: _ROTATOR,
#     pose_queryer.___MOVE_FORWARD_LEFT: _ROTATOR_ACTIVE,
#     pose_queryer.___MOVE_FORWARD_RITE: _ROTATOR_ACTIVE,
#     pose_queryer.___MOVE_BAKWARD_LEFT: _ROTATOR_ACTIVE,
#     pose_queryer.___MOVE_BAKWARD_RITE: _ROTATOR_ACTIVE,
#     pose_queryer.___LOOK_LEFT: _ROTATOR_ACTIVE,
#     pose_queryer.___LOOK_RITE: _ROTATOR_ACTIVE,
#     pose_queryer.___STOP: _ROTATOR,
#     pose_queryer.___ARMED: _ROTATOR,
# }


tracking_points = set([
    BodyPoint.ear_left.value,
    BodyPoint.ear_rite.value,
    BodyPoint.shoulder_left.value,
    BodyPoint.shoulder_rite.value,
    BodyPoint.elbow_left.value,
    BodyPoint.elbow_rite.value,
    BodyPoint.wrist_left.value,
    BodyPoint.wrist_rite.value])

# print (tracking_points)




def show_points(img, idx: int, xc: int, yc: int):
    return img
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
    if point_idx == frame_idx % 13:
        return place_image(img, _POINT_OVERLAY_WHITE_LEFT, (xc, yc), 0, 1, 1)
    return img

def place_image(background, overlay, center_position, angle = 0, size = 1, transparency = 1.0):
    # print (transparency)
    # crpo using
    # https://stackoverflow.com/questions/46273309/using-opencv-how-to-remove-non-object-in-transparent-image
    
    if transparency == 0 or size == 0:
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

    alpha_s = overlay[y_overlay_min:y_overlay_max, x_overlay_min:x_overlay_max, 3] / (1.0 * (255.0 * transparency)) # * transparency
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        background[y_background_min:y_background_max, x_background_min:x_background_max, c] = (
            alpha_s * overlay[y_overlay_min:y_overlay_max, x_overlay_min:x_overlay_max, c] + 
            alpha_l * background[y_background_min:y_background_max, x_background_min:x_background_max, c])

    return background

def get_left_overlay_transparency():
    if pose_queryer.measure.left_hand_active:
        left_overlay_opacity = 1.2
    else:
        left_elbow_threshold_minimum = pose_queryer._ELBOW_ANGLE_LEFT_SIGNAL - pose_queryer._ACTIVE_ELBOW_ANGLE_ERROR 
        left_forearm_angle = round(pose_queryer.measure._left_fore_arm_angle_rel_to_upper_arm)
        if left_forearm_angle > left_elbow_threshold_minimum - 60:
            left_overlay_opacity = max((left_elbow_threshold_minimum - left_forearm_angle)/5.0, 1.0)
        else:
            left_overlay_opacity = 10000
    return left_overlay_opacity

def get_rite_overlay_transparency_fore():
    if pose_queryer.measure.rite_hand_active_fore:
        rite_overlay_opacity_fore = 1.2
    else:
        rite_elbow_threshold_minimum_fore = pose_queryer._ELBOW_ANGLE_RITE_SIGNAL_FORE + pose_queryer._ACTIVE_ELBOW_ANGLE_ERROR 
        rite_forearm_angle_fore = round(pose_queryer.measure._rite_fore_arm_angle_rel_to_upper_arm)
        if rite_forearm_angle_fore < rite_elbow_threshold_minimum_fore + 60:
            rite_overlay_opacity_fore = max((rite_forearm_angle_fore - rite_elbow_threshold_minimum_fore)/5.0, 1.0)
        else:
            rite_overlay_opacity_fore = 10000
    return rite_overlay_opacity_fore

def get_rite_overlay_transparency_back():
    if pose_queryer.measure.rite_hand_active_back:
        rite_overlay_opacity_back = 1.2
    else:
        rite_elbow_threshold_minimum_back = pose_queryer._ELBOW_ANGLE_RITE_SIGNAL_BACK - pose_queryer._ACTIVE_ELBOW_ANGLE_ERROR 
        rite_backarm_angle_back = round(pose_queryer.measure._rite_fore_arm_angle_rel_to_upper_arm)
        if rite_backarm_angle_back > rite_elbow_threshold_minimum_back - 60:
            rite_overlay_opacity_back = max((rite_elbow_threshold_minimum_back - rite_backarm_angle_back)/5.0, 1.0)
        else:
            rite_overlay_opacity_back = 10000
    return rite_overlay_opacity_back

def draw_visual_cues_v2(pose_points: list, img: any, width: int, height: int, pose_action) -> any:
    center = (int(width/2), int(height/2))
    left_elbow_point = pose_points[BodyPoint.elbow_left.value]

    left_shoulder_point = pose_points[BodyPoint.shoulder_left.value]

    left_elbow_plane_point = (0, left_elbow_point[_Y_])
    
    left_upper_arm_angle = pose_queryer.get_angle(left_elbow_plane_point, left_elbow_point, left_shoulder_point)
    activate_overlay_image = _activate_overlay_map[pose_queryer.measure.left_hand_active]

    left_elbow_absolute_angle = -1 * ((left_upper_arm_angle + pose_queryer._ELBOW_ANGLE_LEFT_ACTIVE) % 360)
    left_overlay_opacity = get_left_overlay_transparency()

    motion_image = signal_image_map[pose_action]
    head_rotator_image_index = round(min(13, pose_queryer.measure.nose_from_ear_mid_percent))
    head_rotator_image = pointer_images[head_rotator_image_index]
    img = place_image(img, activate_overlay_image, left_elbow_point, left_elbow_absolute_angle, 0.2, left_overlay_opacity)
    img = place_image(img, motion_image, center, 0, 1, 1.2)
    img = place_image(img, head_rotator_image, center, 360 - round(pose_queryer.measure.angle_between_nose_and_ear_mid), 1, 1.2)

    img = redimension(img, width, height)
    top = round((height * 2) * 0.8)
    img = write_text(-6, top, img, 'nose to ear mid: ' + str(round(pose_queryer.measure._distance_between_nose_and_ear_midpoint)))
    img = write_text(-5, top, img, 'between ears: ' + str(round(pose_queryer.measure._distance_between_ears)))
    img = write_text(-4, top, img, '%: ' + str(round(pose_queryer.measure.nose_from_ear_mid_percent)))
    img = write_text(-3, top, img, 'head angle: ' + str(round(pose_queryer.measure.angle_between_nose_and_ear_mid)))
    img = write_text(-1, top, img, 'fps: ' + pose_queryer.measure.fps)
    img = write_text(0, top, img, 'left upprArm: ' + str(round(pose_queryer.measure._left_uppr_arm_angle)))
    img = write_text(1, top, img, 'left foreArm: ' + str(round(pose_queryer.measure._left_fore_arm_angle)))
    img = write_text(2, top, img, 'left foreArm rel: ' + str(round(pose_queryer.measure._left_fore_arm_angle_rel_to_upper_arm)))

    return img

def redimension(img, width, height):
    return cv2.resize(img, (2*width, 2*height))

def write_text(idx, height, img, text):
    return cv2.putText(
        img, 
        text, 
        (10, height + (idx * 20)), 
        cv2.FONT_HERSHEY_SIMPLEX, 
        0.5, 
        (255, 255, 255), 
        1, 
        cv2.LINE_AA)