import numpy as np

___MOVE_FORWARD: int = 8
___MOVE_BACKWARD: int = 2
___MOVE_FORWARD_LEFT: int = 7
___MOVE_FORWARD_RIGHT: int = 9
___MOVE_BACKWARD_LEFT: int = 1
___MOVE_BACKWARD_RIGHT: int = 3
___LOOK_LEFT: int = 4
___LOOK_RIGHT: int = 6
___STOP: int = 5


@staticmethod
def get_action_for_pose(pose_points: [[]]):
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
def head_is_turned_left(pose_points: [[]]):
    """

    :rtype: bool
    """
    left_ear_distance: float = get_distance_ear_left_from_nose(pose_points)
    right_ear_distance: float = get_distance_ear_right_from_nose(pose_points)
    return (
            right_ear_distance * (head_turn_threshold - head_turn_threshold_error)
            <=
            left_ear_distance
            <=
            right_ear_distance * (head_turn_threshold + head_turn_threshold_error))


@staticmethod
def head_is_turned_right(pose_points: [[]]):
    """

    :rtype: bool
    """
    left_ear_distance: float = get_distance_ear_left_from_nose(pose_points)
    right_ear_distance: float = get_distance_ear_right_from_nose(pose_points)
    return (
            left_ear_distance * (head_turn_threshold - head_turn_threshold_error)
            <=
            right_ear_distance
            <=
            left_ear_distance * (head_turn_threshold + head_turn_threshold_error))


@staticmethod
def body_is_turned_left(pose_points: [[]]):
    """

    :rtype: bool
    """
    left_shoulder_distance: float = get_distance_shoulder_left_from_nose(pose_points)
    right_shoulder_distance: float = get_distance_shoulder_right_from_nose(pose_points)
    return (
            right_shoulder_distance * (body_turn_threshold - body_turn_threshold_error)
            <=
            left_shoulder_distance
            <=
            right_shoulder_distance * (body_turn_threshold + body_turn_threshold_error))


@staticmethod
def body_is_turned_right(pose_points: [[]]):
    """

    :rtype: bool
    """
    left_shoulder_distance: float = get_distance_shoulder_left_from_nose(pose_points)
    right_shoulder_distance: float = get_distance_shoulder_right_from_nose(pose_points)
    return (
            left_shoulder_distance * (body_turn_threshold - body_turn_threshold_error)
            <=
            right_shoulder_distance
            <=
            left_shoulder_distance * (body_turn_threshold + body_turn_threshold_error))


@staticmethod
def left_hand_is_active(pose_points: [[]]):
    """

    :rtype: bool
    """
    left_elbow_angle = get_angle_elbow_left(pose_points)
    return (
            left_elbow_angle >= (active_elbow_angle - active_elbow_angle_error) or
            left_elbow_angle <= (active_elbow_angle + active_elbow_angle_error))


@staticmethod
def right_hand_is_active_forward(pose_points: [[]]):
    """

    :rtype: bool
    """
    right_elbow_angle = get_angle_elbow_right(pose_points)
    return (
            right_elbow_angle >= (active_elbow_angle - active_elbow_angle_error) or
            right_elbow_angle <= (active_elbow_angle + active_elbow_angle_error))


@staticmethod
def right_hand_is_active_backward(pose_points: [[]]):
    """

    :rtype: bool
    """
    right_elbow_angle = get_angle_elbow_right(pose_points)
    return (
            right_elbow_angle >= (active_elbow_angle - active_elbow_angle_error) or
            right_elbow_angle <= (active_elbow_angle + active_elbow_angle_error))


@staticmethod
def get_distance_ear_left_from_nose(pose_points: [[]]):
    """

    :rtype: float
    """
    return get_distance_between_points(
        pose_points,
        BodyPoint.ear_left,
        BodyPoint.nose)


@staticmethod
def get_distance_ear_right_from_nose(pose_points: [[]]):
    """

    :rtype: float
    """
    return get_distance_between_points(
        pose_points,
        BodyPoint.ear_right,
        BodyPoint.nose)


@staticmethod
def get_distance_shoulder_left_from_nose(pose_points: [[]]):
    """

    :rtype: float
    """
    return get_distance_between_points(
        pose_points,
        BodyPoint.shoulder_left,
        BodyPoint.nose)


@staticmethod
def get_distance_shoulder_right_from_nose(pose_points: [[]]):
    """

    :rtype: float
    """
    return get_distance_between_points(
        pose_points,
        BodyPoint.shoulder_right,
        BodyPoint.nose)


@staticmethod
def get_angle_elbow_left(pose_points: [[]]):
    """

    :rtype: float
    """
    return get_angle_between_points(
        pose_points,
        BodyPoint.shoulder_left,
        BodyPoint.elbow_left,
        BodyPoint.wrist_left)


@staticmethod
def get_angle_elbow_right(pose_points: [[]]):
    """

    :rtype: float
    """
    return get_angle_between_points(
        pose_points,
        BodyPoint.shoulder_right,
        BodyPoint.elbow_right,
        BodyPoint.wrist_right)


@staticmethod
def get_distance_between_points(pose_points: [[]], a: BodyPoint, b: BodyPoint):
    """

    :rtype: float
    """
    body_point_a = pose_points[a]
    body_point_b = pose_points[b]
    return get_distance(body_point_a, body_point_b)


@staticmethod
def get_angle_between_points(pose_points: [[]], a: BodyPoint, b: BodyPoint, c: BodyPoint):
    """

    :rtype: float
    """
    body_point_a = pose_points[a]
    body_point_b = pose_points[b]
    body_point_c = pose_points[c]
    return getAngle(body_point_a, body_point_b, body_point_c)


@staticmethod
def get_distance(a: [], b: []):
    """

    :rtype: float
    """
    np.linalg.norm(a - b)


@staticmethod
def get_angle(a: [], b: [], c: []):
    """

    :rtype: float
    """
    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)
    return angle
