# Import TF and TF Hub libraries.
import tensorflow as tf
import tensorflow_hub as hub
import cv2
import numpy as np
import requests
import BodyPoint

# Download the model from TF Hub.
model = hub.load('https://tfhub.dev/google/movenet/singlepose/thunder/3')
movenet = model.signatures['serving_default']
arrow_half = 30

active_elbow_angle = 70
active_elbow_angle_error = 20

body_turn_threshold = 0.8
body_turn_threshold_error = 0.8

head_turn_threshold = 0.75
head_turn_threshold_error = 0.1

url = 'http://***REMOVED***/api/Motion?payload='
# Threshold for 
threshold = .3
print('---------------------------')
print('basic test result: ' + str(requests.get(
    'http://***REMOVED***/api/Motion?payload=%5B%7B%22Item1%22%3A265%2C%22Item2%22%3A95%7D%2C%7B%22Item1%22%3A286%2C%22Item2%22%3A80%7D%2C%7B%22Item1%22%3A258%2C%22Item2%22%3A82%7D%2C%7B%22Item1%22%3A337%2C%22Item2%22%3A85%7D%2C%7B%22Item1%22%3A274%2C%22Item2%22%3A85%7D%2C%7B%22Item1%22%3A391%2C%22Item2%22%3A188%7D%2C%7B%22Item1%22%3A218%2C%22Item2%22%3A177%7D%2C%7B%22Item1%22%3A431%2C%22Item2%22%3A282%7D%2C%7B%22Item1%22%3A199%2C%22Item2%22%3A287%7D%2C%7B%22Item1%22%3A528%2C%22Item2%22%3A269%7D%2C%7B%22Item1%22%3A204%2C%22Item2%22%3A387%7D%2C%7B%22Item1%22%3A343%2C%22Item2%22%3A413%7D%2C%7B%22Item1%22%3A244%2C%22Item2%22%3A411%7D%2C%5D',
    verify=False).text))
print('---------------------------')
# Loads video source (0 is for main webcam)
video_source = 1
cap = cv2.VideoCapture(video_source)

# Checks errors while opening the Video Capture
if not cap.isOpened():
    print('Error loading video')
    quit()

success, img = cap.read()

if not success:
    print('Error reding frame')
    quit()

y, x, _ = img.shape

while success:
    # A frame of video or an image, represented as an int32 tensor of shape: 256x256x3. Channels order: RGB with values in [0, 255].
    tf_img = cv2.resize(img, (256, 256))
    tf_img = cv2.cvtColor(tf_img, cv2.COLOR_BGR2RGB)
    tf_img = np.asarray(tf_img)
    tf_img = np.expand_dims(tf_img, axis=0)

    # Resize and pad the image to keep the aspect ratio and fit the expected size.
    image = tf.cast(tf_img, dtype=tf.int32)
    request_parameter = '['
    # Run model inference.
    outputs = movenet(image)
    # Output is a [1, 1, 17, 3] tensor.
    keypoints = outputs['output_0']
    found_points = 0
    # iterate through keypoints
    for idx, k in enumerate(keypoints[0, 0, :, :]):
        # Converts to numpy array
        k = k.numpy()
        # Checks confidence for keypoint
        if k[2] > threshold:
            found_points = found_points + 1
            # The first two channels of the last dimension represents the yx coordinates (normalized to image frame, i.e. range in [0.0, 1.0]) of the 17 keypoints
            yc = int(k[0] * y)
            xc = int(k[1] * x)
            # print(xc, ',', yc)
            request_parameter = request_parameter + '{"Item1":' + str(xc) + ',"Item2":' + str(yc) + '},'
            # Draws a circle on the image for each keypoint
            # img = cv2.circle(img, (xc, yc), 1, (0, 255, 255), 3)
            # img = cv2.putText(img, str(idx), (xc, yc), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            img = cv2.putText(img, '(' + str(xc) + ',' + str(yc) + ')', (xc - 6, yc + 10), cv2.FONT_HERSHEY_SIMPLEX,
                              0.15, (255, 255, 0), 1, cv2.LINE_AA)

    request_parameter = request_parameter + ']'
    moveChar = 'X'
    if found_points >= 13:
        urlResponse = requests.get(url + request_parameter, verify=False)
        if urlResponse.text == '"5"':
            moveChar = 'O'
            img = cv2.putText(img, str(moveChar), (256, 256), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 8, cv2.LINE_AA)
        if urlResponse.text == '"8"':
            img = cv2.arrowedLine(img, (256, 256 + arrow_half), (256, 256 - arrow_half), (0, 0, 255), 2)
        if urlResponse.text == '"2"':
            img = cv2.arrowedLine(img, (256, 256 - arrow_half), (256, 256 + arrow_half), (0, 0, 255), 2)
        if urlResponse.text == '"4"':
            img = cv2.arrowedLine(img, (256 + arrow_half, 256 + arrow_half), (256 - arrow_half, 256 - arrow_half),
                                  (0, 0, 255), 2)
        if urlResponse.text == '"6"':
            img = cv2.arrowedLine(img, (256 - arrow_half, 256 + arrow_half), (256 + arrow_half, 256 - arrow_half),
                                  (0, 0, 255), 2)
        print('received: ' + str(moveChar))
    else:
        moveChar = 'X'
        img = cv2.putText(img, str(moveChar), (256, 256), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 8, cv2.LINE_AA)
    # Shows image
    cv2.imshow('Movenet', img)
    # Waits for the next frame, checks if q was pressed to quit
    if cv2.waitKey(1) == ord("q"):
        break

    # Reads next frame
    success, img = cap.read()

cap.release()


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


def left_hand_is_active(pose_points: [[]]):
    """

    :rtype: bool
    """
    left_elbow_angle = get_angle_elbow_left(pose_points)
    return (
            left_elbow_angle >= (active_elbow_angle - active_elbow_angle_error) or
            left_elbow_angle <= (active_elbow_angle + active_elbow_angle_error))


def right_hand_is_active(pose_points: [[]]):
    """

    :rtype: bool
    """
    right_elbow_angle = get_angle_elbow_right(pose_points)
    return (
            right_elbow_angle >= (active_elbow_angle - active_elbow_angle_error) or
            right_elbow_angle <= (active_elbow_angle + active_elbow_angle_error))


def get_distance_ear_left_from_nose(pose_points: [[]]):
    """

    :rtype: float
    """
    return get_distance_between_points(
        pose_points,
        BodyPoint.ear_left,
        BodyPoint.nose)


def get_distance_ear_right_from_nose(pose_points: [[]]):
    """

    :rtype: float
    """
    return get_distance_between_points(
        pose_points,
        BodyPoint.ear_right,
        BodyPoint.nose)


def get_distance_shoulder_left_from_nose(pose_points: [[]]):
    """

    :rtype: float
    """
    return get_distance_between_points(
        pose_points,
        BodyPoint.shoulder_left,
        BodyPoint.nose)


def get_distance_shoulder_right_from_nose(pose_points: [[]]):
    """

    :rtype: float
    """
    return get_distance_between_points(
        pose_points,
        BodyPoint.shoulder_right,
        BodyPoint.nose)


def get_angle_elbow_left(pose_points: [[]]):
    """

    :rtype: float
    """
    return get_angle_between_points(
        pose_points,
        BodyPoint.shoulder_left,
        BodyPoint.elbow_left,
        BodyPoint.wrist_left)


def get_angle_elbow_right(pose_points: [[]]):
    """

    :rtype: float
    """
    return get_angle_between_points(
        pose_points,
        BodyPoint.shoulder_right,
        BodyPoint.elbow_right,
        BodyPoint.wrist_right)


def get_distance_between_points(pose_points: [[]], a: BodyPoint, b: BodyPoint):
    """

    :rtype: float
    """
    body_point_a = pose_points[a]
    body_point_b = pose_points[b]
    return get_distance(body_point_a, body_point_b)


def get_angle_between_points(pose_points: [[]], a: BodyPoint, b: BodyPoint, c: BodyPoint):
    """

    :rtype: float
    """
    body_point_a = pose_points[a]
    body_point_b = pose_points[b]
    body_point_c = pose_points[c]
    return getAngle(body_point_a, body_point_b, body_point_c)


def get_distance(a: [], b: []):
    """

    :rtype: float
    """
    np.linalg.norm(a - b)


def get_angle(a: [], b: [], c: []):
    """

    :rtype: float
    """
    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)
    return angle
