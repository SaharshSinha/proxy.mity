# Import TF and TF Hub libraries.
import tensorflow as tf
import tensorflow_hub as hub
import cv2
import numpy as np
import pose_queryer
import time

# Download the model from TF Hub.
model = hub.load('https://tfhub.dev/google/movenet/singlepose/thunder/4')
movenet = model.signatures['serving_default']

# Threshold for 
threshold = .3
# Loads video source (0 is for main webcam)
video_source = 2
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
    pose_points = []
    # A frame of video or an image, represented as an int32 tensor of shape: 256x256x3. Channels order: RGB with values in [0, 255].
    tf_img = cv2.resize(img, (256, 256))
    tf_img = cv2.cvtColor(tf_img, cv2.COLOR_BGR2RGB)
    tf_img = np.asarray(tf_img)
    tf_img = np.expand_dims(tf_img, axis=0)

    # Resize and pad the image to keep the aspect ratio and fit the expected size.
    image = tf.cast(tf_img, dtype=tf.int32)
    
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
            found_points += 1 # = found_points + 1
            # The first two channels of the last dimension represents the yx coordinates (normalized to image frame, i.e. range in [0.0, 1.0]) of the 17 keypoints
            yc = int(k[0] * y)
            xc = int(k[1] * x)

            # if found_points == 5:
            #     print (str(xc), '; ', str(yc), '; ', str(k[1]), '; ', str(k[0]))
            
            pose_points.append([xc, yc])
            img = cv2.putText(
                img, 
                '(' + str(xc) + ',' + str(yc) + ')', 
                (xc - 6, yc + 10), 
                cv2.FONT_HERSHEY_SIMPLEX,
                0.15, 
                (255, 255, 0), 
                1, 
                cv2.LINE_AA)

    # request_parameter = request_parameter + ']'
    moveChar = 'X'
    if found_points >= 13:
        pose_action = pose_queryer.get_action_for_pose(pose_points)
        moveChar = str(pose_action)
        print(moveChar)

    img = cv2.putText(img, str(moveChar), (256, 256), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 8, cv2.LINE_AA)
    cv2.imshow('Movenet', img)
    # Waits for the next frame, checks if q was pressed to quit
    if cv2.waitKey(1) == ord("q"):
        break

    # Reads next frame
    success, img = cap.read()
    
    time.sleep(0.5)

cap.release()

