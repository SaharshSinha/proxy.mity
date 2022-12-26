import cv2
import time

def place_image(background, overlay, center_position, angle = 0, size = 0, opacity = 1):
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
    
    rotate_matrix    = cv2.getRotationMatrix2D(center=center, angle=rotat_angle, scale=1)
    overlay_rotated  = cv2.warpAffine(src=overlay, M=rotate_matrix, dsize=(width, height))
    alpha_s = overlay_rotated[y_overlay_min:y_overlay_max, x_overlay_min:x_overlay_max, 3] / 255.0 * opacity
    alpha_l = 1.0 - alpha_s

    # print()
    # print()
    for c in range(0, 3):
        # print('x_min: ', x_min, '; x_max: ', x_max, '; y_min: ', y_min, '; y_max: ', y_max)
        # print('x_background_min: ', x_background_min, '; x_background_max: ', x_background_max, '; y_background_min: ', y_background_min, '; y_background_max: ', y_background_max)
        # print('x_min_delta: ', x_min_delta, '; x_max_delta: ', x_max_delta, '; y_min_delta: ', y_min_delta, '; y_max_delta: ', y_max_delta)
        # print('x_overlay_min: ', x_overlay_min, '; x_overlay_max: ', x_overlay_max, '; y_overlay_min: ', y_overlay_min, '; y_overlay_max: ', y_overlay_max)
        # print((alpha_s * overlay_rotated[y_overlay_min:y_overlay_max, x_overlay_min:x_overlay_max, c]).shape)
        # print((alpha_l * background[y_background_min:y_background_max, x_background_min:x_background_max, c]).shape)
        # print()
        # background[y_min:y_max, x_min:x_max, c] = (alpha_s * overlay_rotated[:, :, c] + alpha_l * background[y_min:y_max, x_min:x_max, c])
        background[y_background_min:y_background_max, x_background_min:x_background_max, c] = (
            alpha_s * overlay_rotated[y_overlay_min:y_overlay_max, x_overlay_min:x_overlay_max, c] + 
            alpha_l * background[y_background_min:y_background_max, x_background_min:x_background_max, c])

    

video_source = 2
cap = cv2.VideoCapture(video_source)
overlayed = cv2.cvtColor(cv2.imread('images/arrow.png'), cv2.COLOR_RGB2RGBA)
# overlayed1 = cv2.cvtColor(cv2.imread('images/triangle.png'), cv2.COLOR_RGB2RGBA)
overlayed1 = cv2.imread('images/triangle.png', -1)
# dividing height and width by 2 to get the center of the image
height, width = overlayed1.shape[:2]
# get the center coordinates of the image to create the 2D rotation matrix
center = (width/2, height/2)

rotat_angle = 0.2

# using cv2.getRotationMatrix2D() to get the rotation matrix
rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=rotat_angle, scale=1)
 
# rotate the image using cv2.warpAffine
overlayed1 = cv2.warpAffine(src=overlayed1, M=rotate_matrix, dsize=(width, height))
# cv2.imshow('overlayed1', overlayed1)
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

# print (img)
# print (overlayed1)



# cv2.imshow('proxyMotion2', img)

alpha = 0.7
beta = (1.0 - alpha)

center_x = img.shape[1]
center_y = img.shape[0]

ofset = 0
counter = 1
while success:
    ofset -= 1
    img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
    img = cv2.resize(img, (2*x, 2*y))
    
    place_image(
        img,
        overlayed1,
        (center_x + ofset, center_y + ofset),
        rotat_angle,
        1,
        (counter%10)/10)

    cv2.imshow('proxyMotion', img)
    rotat_angle = rotat_angle + .2
    if cv2.waitKey(1) == ord("q"):
        break

    success, img = cap.read()
    img = cv2.flip(img, 1)
    counter+=1
    # time.sleep(0.2)
    

cap.release()
cv2.destroyAllWindows()