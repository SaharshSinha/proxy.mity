import math
from body_points import BodyPoint

___MOVE_FORWARD: int = 8
___MOVE_BACKWARD: int = 2
___MOVE_FORWARD_LEFT: int = 7
___MOVE_FORWARD_RIGHT: int = 9
___MOVE_BACKWARD_LEFT: int = 1
___MOVE_BACKWARD_RIGHT: int = 3
___LOOK_LEFT: int = 4
___LOOK_RIGHT: int = 6
___STOP: int = 5

arrow_half = 30

active_elbow_angle = 70
active_elbow_angle_error = 20

body_turn_threshold = 0.8
body_turn_threshold_error = 0.8

head_turn_threshold = 0.75
head_turn_threshold_error = 0.1


@staticmethod
def get_action_for_pose(pose_points) -> int:
    if left_hand_is_active(pose_points):
        if head_is_turned_left(pose_points):
            return ___LOOK_LEFT
        elif head_is_turned_right(pose_points):
            return ___LOOK_RIGHT
        elif right_hand_is_active_forward(pose_points):
            if body_is_turned_left(pose_points):
                return ___MOVE_FORWARD_LEFT
            elif body_is_turned_right(pose_points):
                return ___MOVE_FORWARD_RIGHT
            else:
                return ___MOVE_FORWARD
        elif right_hand_is_active_backward(pose_points):
            if body_is_turned_left(pose_points):
                return ___MOVE_BACKWARD_LEFT
            elif body_is_turned_right(pose_points):
                return ___MOVE_BACKWARD_RIGHT
            else:
                return ___MOVE_BACKWARD
        else:
            return ___STOP
    else:
        return ___STOP


@staticmethod
def head_is_turned_left(pose_points) -> bool:
    """

    :rtype: bool
    """
    left_ear_distance: float = get_distance_ear_left_from_nose(pose_points)
    right_ear_distance: float = get_distance_ear_right_from_nose(pose_points)
    print ('left_ear_distance: ', str(left_ear_distance), '; right_ear_distance: ', str(right_ear_distance))
    return (
            right_ear_distance * (head_turn_threshold - head_turn_threshold_error)
            <=
            left_ear_distance
            <=
            right_ear_distance * (head_turn_threshold + head_turn_threshold_error))


@staticmethod
def head_is_turned_right(pose_points) -> bool:
    """

    :rtype: bool
    """
    left_ear_distance: float = get_distance_ear_left_from_nose(pose_points)
    right_ear_distance: float = get_distance_ear_right_from_nose(pose_points)
    print ('left_ear_distance: ', str(left_ear_distance), '; right_ear_distance: ', str(right_ear_distance))
    return (
            left_ear_distance * (head_turn_threshold - head_turn_threshold_error)
            <=
            right_ear_distance
            <=
            left_ear_distance * (head_turn_threshold + head_turn_threshold_error))


@staticmethod
def body_is_turned_left(pose_points) -> bool:
    """

    :rtype: bool
    """
    left_shoulder_distance: float = get_distance_shoulder_left_from_nose(pose_points)
    right_shoulder_distance: float = get_distance_shoulder_right_from_nose(pose_points)
    print ('left_shoulder_distance: ', str(left_shoulder_distance), '; right_shoulder_distance: ', str(right_shoulder_distance))
    return (
            right_shoulder_distance * (body_turn_threshold - body_turn_threshold_error)
            <=
            left_shoulder_distance
            <=
            right_shoulder_distance * (body_turn_threshold + body_turn_threshold_error))


@staticmethod
def body_is_turned_right(pose_points) -> bool:
    """

    :rtype: bool
    """
    left_shoulder_distance: float = get_distance_shoulder_left_from_nose(pose_points)
    right_shoulder_distance: float = get_distance_shoulder_right_from_nose(pose_points)
    print ('left_shoulder_distance: ', str(left_shoulder_distance), '; right_shoulder_distance: ', str(right_shoulder_distance))
    return (
            left_shoulder_distance * (body_turn_threshold - body_turn_threshold_error)
            <=
            right_shoulder_distance
            <=
            left_shoulder_distance * (body_turn_threshold + body_turn_threshold_error))


@staticmethod
def left_hand_is_active(pose_points) -> bool:
    """

    :rtype: bool
    """
    left_elbow_angle = get_angle_elbow_left(pose_points)
    print ('left_elbow_angle: ', str(left_elbow_angle))
    return (
            left_elbow_angle >= (active_elbow_angle - active_elbow_angle_error) or
            left_elbow_angle <= (active_elbow_angle + active_elbow_angle_error))


@staticmethod
def right_hand_is_active_forward(pose_points) -> bool:
    """

    :rtype: bool
    """
    right_elbow_angle = get_angle_elbow_right(pose_points)
    print ('right_elbow_angle: ', str(right_elbow_angle))
    return (
            right_elbow_angle >= (active_elbow_angle - active_elbow_angle_error) or
            right_elbow_angle <= (active_elbow_angle + active_elbow_angle_error))


@staticmethod
def right_hand_is_active_backward(pose_points) -> bool:
    """

    :rtype: bool
    """
    right_elbow_angle = get_angle_elbow_right(pose_points)
    print ('right_elbow_angle: ', str(right_elbow_angle))
    return (
            right_elbow_angle >= (active_elbow_angle - active_elbow_angle_error) or
            right_elbow_angle <= (active_elbow_angle + active_elbow_angle_error))


@staticmethod
def get_distance_ear_left_from_nose(pose_points) -> float:
    """

    :rtype: float
    """
    return get_distance_between_points(
        pose_points,
        BodyPoint.ear_left,
        BodyPoint.nose)


@staticmethod
def get_distance_ear_right_from_nose(pose_points) -> float:
    """

    :rtype: float
    """
    return get_distance_between_points(
        pose_points,
        BodyPoint.ear_rite,
        BodyPoint.nose)


@staticmethod
def get_distance_shoulder_left_from_nose(pose_points) -> float:
    """

    :rtype: float
    """
    return get_distance_between_points(
        pose_points,
        BodyPoint.shoulder_left,
        BodyPoint.nose)


@staticmethod
def get_distance_shoulder_right_from_nose(pose_points) -> float:
    """

    :rtype: float
    """
    return get_distance_between_points(
        pose_points,
        BodyPoint.shoulder_rite,
        BodyPoint.nose)


@staticmethod
def get_angle_elbow_left(pose_points) -> float:
    """

    :rtype: float
    """
    return get_angle_between_points(
        pose_points,
        BodyPoint.shoulder_left,
        BodyPoint.elbow_left,
        BodyPoint.wrist_left)


@staticmethod
def get_angle_elbow_right(pose_points) -> float:
    """

    :rtype: float
    """
    return get_angle_between_points(
        pose_points,
        BodyPoint.shoulder_rite,
        BodyPoint.elbow_rite,
        BodyPoint.wrist_rite)


@staticmethod
def get_distance_between_points(pose_points, a: BodyPoint, b: BodyPoint) -> float:
    """

    :rtype: float
    """
    body_point_a = pose_points[a.value]
    body_point_b = pose_points[b.value]
    return get_distance(body_point_a, body_point_b)


@staticmethod
def get_angle_between_points(pose_points, a: BodyPoint, b: BodyPoint, c: BodyPoint) -> float:
    """

    :rtype: float
    """
    body_point_a = pose_points[a.value]
    body_point_b = pose_points[b.value]
    body_point_c = pose_points[c.value]
    return get_angle(body_point_a, body_point_b, body_point_c)


@staticmethod
def get_distance(a, b) -> float:
    """

    :rtype: float
    """
    return math.dist(a, b)


@staticmethod
def get_angle(a, b, c) -> float:
    """

    :rtype: float
    """
    return math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
