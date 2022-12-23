# Import TF and TF Hub libraries.
import tensorflow as tf
import tensorflow_hub as hub
import cv2
import numpy as np
import pose_queryer
import time
import requests
import matplotlib.pyplot as plt
from PIL import Image

relay_host = '***REMOVED***'
# Threshold for 
threshold = .3
# Loads video source (0 is for main webcam)
video_source = 2
cap = cv2.VideoCapture(video_source)
overlayed = cv2.cvtColor(cv2.imread('images/arrow.png'), cv2.COLOR_RGB2RGBA)
# Checks errors while opening the Video Capture
if not cap.isOpened():
    print('Error loading video')
    quit()

success, img = cap.read()
if not success:
    print('Error reding frame')
    quit()

img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
y, x, _ = img.shape
prev_move_char = '5'
print('got first image: ', img.shape)
print('overlayed:       ', overlayed.shape)

cv2.imshow('proxyMotion', img)


# Download the model from TF Hub.
# model = hub.load('https://tfhub.dev/google/movenet/singlepose/thunder/4')
model = hub.load('D:\Downloads\movenet')
movenet = model.signatures['serving_default']

alpha = 0.7
beta = (1.0 - alpha)
while success:
    pose_points = []
    img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
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
            
            pose_points.append([xc, yc])
            img = pose_queryer.show_points(img, idx, xc, yc)
            # img = cv2.putText(
            #     img, 
            #     '(' + str(xc) + ',' + str(yc) + ')', 
            #     (xc - 6, yc + 10), 
            #     cv2.FONT_HERSHEY_SIMPLEX,
            #     0.15, 
            #     point_color, 
            #     1, 
            #     cv2.LINE_AA)

    # request_parameter = request_parameter + ']'
    move_char = 'X'
    if found_points >= 13:
        pose_action = pose_queryer.get_action_for_pose(pose_points)
        move_char = str(pose_action)
        # print(move_char)
        img = pose_queryer.draw_visual_cues_v1(pose_points, img, x, y)
    else:
        move_char = '5'
    # if move_char != prev_move_char:
    # ---http_resp = requests.get('http://'+relay_host+'/api/Conveyer/' + move_char)
        # if (http_resp.ok):
        #     prev_move_char = move_char
    
    
    img = cv2.putText(img, str(move_char), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 8, cv2.LINE_AA)
    img = cv2.resize(img, (2*x, 2*y))
    # img = pose_queryer.overlay(img, overlayed)
    
    dst = cv2.addWeighted( img, alpha, overlayed, beta, 0.0)
    # img = Image.fromarray(img) # Image.open(r"BACKGROUND_IMAGE_PATH")
    # fore_image = Image.fromarray(overlayed)
    # img.paste(fore_image, (0,0), mask = overlayed)
    # img = np.asarray(img)
    
    cv2.imshow('proxyMotion', dst)
    # cv2.imshow('overlayed', overlayed)
    # Waits for the next frame, checks if q was pressed to quit
    if cv2.waitKey(1) == ord("q"):
        break

    # Reads next frame
    success, img = cap.read()
    img = cv2.flip(img, 1)
    
    # plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA))
    # plt.show()
    # img_window.set_data(img)
    # plt.draw()
    # plt.show()
    # time.sleep(0.5)

cap.release()
cv2.destroyAllWindows()

def create_overlay(back_img, fore_img):
    back_image = Image.fromarray(back_img) # Image.open(r"BACKGROUND_IMAGE_PATH")
    fore_image = Image.fromarray(fore_img)
    back_image.paste(fore_image, (0,0), mask = fore_img)
    return np.asarray(back_image)




