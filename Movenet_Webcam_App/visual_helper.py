
from math import sin, cos, radians, pi, atan2, degrees, dist
from body_points import BodyPoint, BodyPointColor, color_array
import cv2
import pose_queryer

_X_ = 0
_Y_ = 1

_FOREARM_OVERLAY_WHITE = cv2.imread('images/triangle.png', -1)
_POINT_OVERLAY_WHITE_LEFT = cv2.imread('images/point.png', -1)

_ROTATOR = cv2.imread('images/rotator-radial.10.png', -1)
_ROTATOR_ACTIVE = cv2.imread('images/rotator-radial-active.10.png', -1)

_FORWARD = cv2.imread('images/forward.56.png', -1)
_FORWARD_LEFT = cv2.imread('images/forward-left.56.png', -1)
_FORWARD_RITE = cv2.imread('images/forward-rite.56.png', -1)

_BACKWARD = cv2.imread('images/backward.56.png', -1)
_BACKWARD_LEFT = cv2.imread('images/backward-left.56.png', -1)
_BACKWARD_RITE = cv2.imread('images/backward-rite.56.png', -1)

_TURN_LEFT = cv2.imread('images/turn-left.56.png', -1)
_TURN_RITE = cv2.imread('images/turn-rite.56.png', -1)

_NO_GO = cv2.imread('images/no-go.56.png', -1)

_INFONT_SIZE = 1
_INFONT_COLOR = 1
_INFONT_X = 1
_INFONT_Y = 1


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

rotator_image_map = {
    pose_queryer.___MOVE_FORWARD: _ROTATOR,
    pose_queryer.___MOVE_BAKWARD: _ROTATOR,
    pose_queryer.___MOVE_FORWARD_LEFT: _ROTATOR_ACTIVE,
    pose_queryer.___MOVE_FORWARD_RITE: _ROTATOR_ACTIVE,
    pose_queryer.___MOVE_BAKWARD_LEFT: _ROTATOR_ACTIVE,
    pose_queryer.___MOVE_BAKWARD_RITE: _ROTATOR_ACTIVE,
    pose_queryer.___LOOK_LEFT: _ROTATOR_ACTIVE,
    pose_queryer.___LOOK_RITE: _ROTATOR_ACTIVE,
    pose_queryer.___STOP: _ROTATOR,
    pose_queryer.___ARMED: _ROTATOR,
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


def draw_visual_cues_v2(pose_points: list, img: any, width: int, height: int, pose_action) -> any:
    left_elbow_point = pose_points[BodyPoint.elbow_left.value]
    rite_elbow_point = pose_points[BodyPoint.elbow_rite.value]

    left_shoulder_point = pose_points[BodyPoint.shoulder_left.value]
    rite_shoulder_point = pose_points[BodyPoint.shoulder_rite.value]

    left_elbow_plane_point = (0, left_elbow_point[_Y_])
    rite_elbow_plane_point = (0, rite_elbow_point[_Y_])
    
    left_upper_arm_angle = pose_queryer.get_angle(left_elbow_plane_point, left_elbow_point, left_shoulder_point)
    rite_upper_arm_angle = pose_queryer.get_angle(rite_elbow_plane_point, rite_elbow_point, rite_shoulder_point)

    # left_elbow_angle = get_angle_elbow_left(pose_points)
    # rite_elbow_angle = get_angle_elbow_rite(pose_points)

    left_elbow_absolute_angle = -1 * ((left_upper_arm_angle + pose_queryer._ELBOW_ANGLE_LEFT_ACTIVE) % 360)
    rite_elbow_absolute_angle_fore = -1 * ((rite_upper_arm_angle + pose_queryer._ELBOW_ANGLE_RITE_ACTIVE_FORE) % 360)
    rite_elbow_absolute_angle_back = -1 * ((rite_upper_arm_angle + pose_queryer._ELBOW_ANGLE_RITE_ACTIVE_BACK) % 360)

    if pose_queryer.measure._rite_fore_arm_angle > 90 and pose_queryer.measure._rite_fore_arm_angle < 270:
        rite_elbow_absolute_angle = rite_elbow_absolute_angle_fore
    else:
        rite_elbow_absolute_angle = rite_elbow_absolute_angle_back

        
    
    # motion_image = signal_image_map[pose_queryer.get_action_for_pose_v2(pose_points=pose_points)]
    motion_image = signal_image_map[pose_action]
    rotator_image = rotator_image_map[pose_action]
    head_rotation_angle = (
        10 * 6.5 * -1 * 2 * 
        (pose_queryer.measure._left_ear_distance_from_nose - pose_queryer.measure._rite_ear_distance_from_nose) / 
        max(pose_queryer.measure._left_ear_distance_from_nose, pose_queryer.measure._rite_ear_distance_from_nose)
    )

    img = place_image(img, _FOREARM_OVERLAY_WHITE, left_elbow_point, left_elbow_absolute_angle, 1, 1)
    img = place_image(img, _FOREARM_OVERLAY_WHITE, rite_elbow_point, rite_elbow_absolute_angle, 1, 1)
    img = place_image(img, motion_image, (int(width/2), int(height/2)))
    img = place_image(img, rotator_image, (int(width/2), int(height/2)), head_rotation_angle)

    img = redimension(img, width, height)
    top = round((height * 2) * 0.8)
    img = write_text(-2, top, img, 'head_rotation_angle: ' + str(round(head_rotation_angle)))
    img = write_text(-1, top, img, 'fps: ' + pose_queryer.measure.fps)
    img = write_text(0, top, img, 'left upprArm: ' + str(round(pose_queryer.measure._left_uppr_arm_angle)))
    img = write_text(1, top, img, 'left foreArm: ' + str(round(pose_queryer.measure._left_fore_arm_angle)))
    img = write_text(2, top, img, 'left foreArm rel: ' + str(round(pose_queryer.measure._left_fore_arm_angle_rel_to_upper_arm)))
    img = write_text(3, top, img, 'rite upprArm: ' + str(round(pose_queryer.measure._rite_uppr_arm_angle)))
    img = write_text(4, top, img, 'rite foreArm: ' + str(round(pose_queryer.measure._rite_fore_arm_angle)))
    img = write_text(5, top, img, 'rite foreArm rel: ' + str(round(pose_queryer.measure._rite_fore_arm_angle_rel_to_upper_arm)))
    img = write_text(6, top, img, 'left ear to nose: ' + str(round(pose_queryer.measure._left_ear_distance_from_nose)))
    img = write_text(7, top, img, 'rite ear to nose: ' + str(round(pose_queryer.measure._rite_ear_distance_from_nose)))

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