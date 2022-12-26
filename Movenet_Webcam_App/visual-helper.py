
from math import sin, cos, radians, pi, atan2, degrees, dist
from body_points import BodyPoint, BodyPointColor, color_array
import cv2
import pose_queryer

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
    
    # crpo using
    # https://stackoverflow.com/questions/46273309/using-opencv-how-to-remove-non-object-in-transparent-image
    
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

