import cv2

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

x_offset = int((img.shape[1] - overlayed1.shape[1])/2)
y_offset = int((img.shape[0] - overlayed1.shape[0])/2)

y1, y2 = y_offset, y_offset + overlayed1.shape[0]
x1, x2 = x_offset, x_offset + overlayed1.shape[1]

ofset = -30

while success:
    ofset += 1
    img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
    img = cv2.resize(img, (2*x, 2*y))
        
    rotate_matrix       = cv2.getRotationMatrix2D(center=center, angle=rotat_angle, scale=1)
    overlayed1_rotated  = cv2.warpAffine(src=overlayed1, M=rotate_matrix, dsize=(width, height))

    alpha_s = overlayed1_rotated[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        img[y1+ofset:y2+ofset, x1+ofset:x2+ofset, c] = (alpha_s * overlayed1_rotated[:, :, c] + alpha_l * img[y1+ofset:y2+ofset, x1+ofset:x2+ofset, c])
        # print ('---')
        # print (img[y1:y2, x1:x2, c])
    
    # cv2.imshow('img[y1:y2, x1:x2, c]', img[y1:y2, x1:x2, c])
    # dst = cv2.addWeighted(img, alpha, overlayed, beta, 0.0)
    cv2.imshow('proxyMotion', img)
    # cv2.imshow('overlayed1', overlayed1)
    rotat_angle = rotat_angle + .2
    if cv2.waitKey(1) == ord("q"):
        break

    success, img = cap.read()
    img = cv2.flip(img, 1)


cap.release()
cv2.destroyAllWindows()