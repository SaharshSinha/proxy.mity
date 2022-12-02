import math
from body_points import BodyPoint

___MOVE_FORWARD: int = 8
___MOVE_BAKWARD: int = 2
___MOVE_FORWARD_LEFT: int = 7
___MOVE_FORWARD_RITE: int = 9
___MOVE_BAKWARD_LEFT: int = 1
___MOVE_BAKWARD_RITE: int = 3
___LOOK_LEFT: int = 4
___LOOK_RITE: int = 6
___STOP: int = 5

arrow_half = 30

elbow_angle_left_active = 270
elbow_angle_left_signal = 270 + 45

elbow_angle_rite_active = 90
elbow_angle_rite_signal = 90 - 45

active_elbow_angle_error = 15

body_tilt_threshold = 0.15

head_turn_threshold = 0.5
head_turn_threshold_error = 0.1


def get_action_for_pose(pose_points) -> int:
    if left_hand_is_active(pose_points):
        if head_is_turned_left(pose_points):
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
        if head_is_turned_left(pose_points):
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
    rite_ear_min_distance = rite_ear_distance * (head_turn_threshold - head_turn_threshold_error)
    rite_ear_max_distance = rite_ear_distance * (head_turn_threshold + (head_turn_threshold_error * 3))
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
    left_ear_min_distance = left_ear_distance * (head_turn_threshold - head_turn_threshold_error)
    left_ear_max_distance = left_ear_distance * (head_turn_threshold + (head_turn_threshold_error*3))
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
    return (shoulder_height_difference >= (shoulder_distance * body_tilt_threshold))


def body_is_tilted_rite(pose_points) -> bool:
    """

    :rtype: bool
    """
    shoulder_distance: float = get_distance_between_shoulders(pose_points)
    shoulder_height_difference = get_diffrence_between_shoulder_heights(pose_points) * -1
    # print ('        shoulder_distance: ', str(shoulder_distance))
    # print ('        shoulder_height_difference: ', str(shoulder_height_difference))
    # print ('        -----')
    return (shoulder_height_difference >= (shoulder_distance * body_tilt_threshold))


def left_hand_is_active(pose_points) -> bool:
    """

    :rtype: bool
    """
    left_elbow_angle = get_angle_elbow_left(pose_points)
    # print ('left_elbow_angle: ', str(left_elbow_angle))
    return (
            left_elbow_angle >= (elbow_angle_left_active - active_elbow_angle_error) and
            left_elbow_angle <= (elbow_angle_left_active + active_elbow_angle_error))



def left_hand_is_signalling(pose_points) -> bool:
    """

    :rtype: bool
    """
    left_elbow_angle = get_angle_elbow_left(pose_points)
    # print ('left_elbow_angle: ', str(left_elbow_angle))
    return (
            left_elbow_angle >= (elbow_angle_left_signal - active_elbow_angle_error) and
            left_elbow_angle <= (elbow_angle_left_signal + active_elbow_angle_error))



def rite_hand_is_active(pose_points) -> bool:
    """

    :rtype: bool
    """
    rite_elbow_angle = get_angle_elbow_rite(pose_points)
    # print ('rite_elbow_angle: ', str(rite_elbow_angle))
    return (
            rite_elbow_angle >= (elbow_angle_rite_active - active_elbow_angle_error) and
            rite_elbow_angle <= (elbow_angle_rite_active + active_elbow_angle_error))


def rite_hand_is_signalling(pose_points) -> bool:
    """

    :rtype: bool
    """
    rite_elbow_angle = get_angle_elbow_rite(pose_points)
    # print ('    rite_elbow_angle: ', str(rite_elbow_angle))
    # print ('    -----')
    return (
            rite_elbow_angle >= (elbow_angle_rite_signal - active_elbow_angle_error) and
            rite_elbow_angle <= (elbow_angle_rite_signal + active_elbow_angle_error))


# def rite_hand_is_active_bakward(pose_points) -> bool:
#     """

#     :rtype: bool
#     """
#     rite_elbow_angle = get_angle_elbow_rite(pose_points)
#     return (
#             rite_elbow_angle >= (elbow_angle_rite_signal - active_elbow_angle_error) and
#             rite_elbow_angle <= (elbow_angle_rite_signal + active_elbow_angle_error))


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



def get_distance_between_shoulders(pose_points) -> float:
    """

    :rtype: float
    """
    return get_distance_between_points(
        pose_points,
        BodyPoint.shoulder_left,
        BodyPoint.shoulder_rite)


def get_diffrence_between_shoulder_heights(pose_points) -> float:
    """

    :rtype: float
    """
    return (pose_points[BodyPoint.shoulder_left.value][1] - pose_points[BodyPoint.shoulder_rite.value][1])


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
    normalized_body_point = [ body_point_bx[0], (body_point_by1[1] + body_point_by2[1]) / 2]
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
    return math.dist(a, b)


def get_angle(a, b, c) -> float:
    """

    :rtype: float
    """
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang
