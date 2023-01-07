# Import TF and TF Hub libraries.
import tensorflow as tf
import tensorflow_hub as hub
import cv2
import numpy as np
import pose_queryer
import visual_helper
import os
import requests
import matplotlib.pyplot as plt
from PIL import Image
import time
from datetime import datetime

video_source = 0


# Download the model from TF Hub.
# model = hub.load('https://tfhub.dev/google/movenet/singlepose/thunder/4')
model = hub.load('D:\Downloads\movenet')
movenet = model.signatures['serving_default']
relay_host = '***REMOVED***'

os.system('cls')
frame_number = 0
threshold = .3
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
frame_idx = 0
alpha = 0.7
beta = (1.0 - alpha)
prev_frame_time = 0
new_frame_time = 0
dir_name = 'c:\\temp\\' + datetime.now().strftime("%H_%M_%S")
os.mkdir(dir_name)
print(dir_name)
all_frames = []
frame_write_batch_size = -1

while success:
    new_frame_time = time.time()
    fps = str(int(1/(new_frame_time-prev_frame_time)))
    prev_frame_time = new_frame_time
    pose_queryer.measure.fps = fps
    frame_idx += 1
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
    for point_idx, k in enumerate(keypoints[0, 0, :, :]):
        # Converts to numpy array
        k = k.numpy()
        # Checks confidence for keypoint
        if k[2] > threshold:
            found_points += 1 # = found_points + 1
            # The first two channels of the last dimension represents the yx coordinates (normalized to image frame, i.e. range in [0.0, 1.0]) of the 17 keypoints
            yc = int(k[0] * y)
            xc = int(k[1] * x)
            
            pose_points.append([xc, yc])
            img = visual_helper.show_points_v2(img, frame_idx, point_idx, xc, yc)
            
    # request_parameter = request_parameter + ']'
    move_char = 'X'
    if found_points >= 13:
        pose_action = pose_queryer.get_action_for_pose_v2(pose_points)
        move_char = str(pose_action)
        # print(move_char)
        img = visual_helper.draw_visual_cues_v2(pose_points, img, x, y, pose_action)
    else:
        move_char = '5'
    # if move_char != prev_move_char:
    # http_resp = requests.get('http://'+relay_host+'/api/Conveyer/' + move_char)
        # if (http_resp.ok):
        #     prev_move_char = move_char
    
    # img = cv2.putText(img, str(move_char), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 8, cv2.LINE_AA)
    img = cv2.resize(img, (2*x, 2*y))
    
    cv2.imshow('proxyMotion', img)
    
    if frame_write_batch_size > 0:
        all_frames.append(img)
        if len(all_frames) >= 2000:
            print('offloading images')
            while (len(all_frames) > 0):
                frame_number += 1
                frame = all_frames.pop()
                cv2.imwrite(dir_name + '\\' + str(f'{frame_number:05}') + '.png', frame)
                print('saved frame ' + str(frame_number))    

    if cv2.waitKey(1) == ord("q"):
        break

    # Reads next frame
    success, img = cap.read()
    img = cv2.flip(img, 1)

cap.release()
cv2.destroyAllWindows()

def create_overlay(back_img, fore_img):
    back_image = Image.fromarray(back_img) # Image.open(r"BACKGROUND_IMAGE_PATH")
    fore_image = Image.fromarray(fore_img)
    back_image.paste(fore_image, (0,0), mask = fore_img)
    return np.asarray(back_image)




