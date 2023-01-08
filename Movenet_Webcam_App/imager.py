import cv2
import time

out_dir = 'images/pointers/temp/'
template_dir = 'images/templates/'
base = cv2.imread('images/templates/pointer_base.png', -1)
height, width, _ = base.shape
center = (round(width/2), round(height/2))
pointer_01 = cv2.imread('images/templates/pointer_1.png', -1)
pointer_02 = cv2.imread('images/templates/pointer_2.png', -1)
pointer_03 = cv2.imread('images/templates/pointer_3.png', -1)
pointer_04 = cv2.imread('images/templates/pointer_4.png', -1)
pointer_05 = cv2.imread('images/templates/pointer_5.png', -1)
pointer_06 = cv2.imread('images/templates/pointer_6.png', -1)
pointer_07 = cv2.imread('images/templates/pointer_7.png', -1)
pointer_08 = cv2.imread('images/templates/pointer_8.png', -1)
pointer_09 = cv2.imread('images/templates/pointer_9.png', -1)
pointer_10 = cv2.imread('images/templates/pointer_10.png', -1)
pointer_11 = cv2.imread('images/templates/pointer_11.png', -1)
pointer_12 = cv2.imread('images/templates/pointer_12.png', -1)
pointer_13 = cv2.imread('images/templates/pointer_13.png', -1)

pointers = [pointer_01, pointer_02, pointer_03, pointer_04, pointer_05, pointer_06, pointer_07, pointer_08, pointer_09, pointer_10, pointer_11, pointer_12, pointer_13] 
# pointers = []
# def create_pointers():
#     for i in range(1, 14):
#         pointer_img = cv2.line(
#             base, 
#             (0, round(height/2)-1),
#             (round(width * (15-i)/100), round(height/2)),
#             (255, 255, 255),
#             3)
#         new_file = template_dir + 'pointer_' + str(i) + '.png'
#         cv2.imwrite(new_file, pointer_img)
#         pointers.append(pointer_img)
#         print('created template: '+ new_file)

def main():
    angle = 15
    # create_pointers()
    new_files = []
    pointer_images = []
    for i in range(1, 15):
        
        base_template = cv2.imread('images/templates/pointer_base.png', -1)
        pointer_img = cv2.cvtColor(base_template, cv2.COLOR_RGB2RGBA)
        pointer_img = place_image(base_template, pointers[0], center)
        for j in range (1, len(pointers)):
            pointer = pointers[j]
            pointer_img = place_image(pointer_img, pointer, center, (angle*j))
            pointer_img = place_image(pointer_img, pointer, center, 360 - (angle*j))
        angle -= 1
        new_file = out_dir + 'pointer_' + str(i) + '.png'
        
        cv2.imwrite(new_file, cv2.cvtColor(pointer_img, cv2.COLOR_RGBA2RGB))
        new_files.append(pointer_img)
        print('created pointer: '+ new_file)
    print('new files len:' + str(len(new_files)))
    
    for i in range(20):
        for new_file in new_files:
            cv2.imshow('new_file', new_file)
            time.sleep(0.016)
            # print(new_file)
            if cv2.waitKey(1) == ord("q"):
                break
            print(i)


    

def place_image(background, overlay, center_position, angle = 0, size = 1, transparency = 1.0):
    # print (transparency)
    # crpo using
    # https://stackoverflow.com/questions/46273309/using-opencv-how-to-remove-non-object-in-transparent-image
    
    if transparency == 0 or size == 0:
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

    alpha_s = overlay[y_overlay_min:y_overlay_max, x_overlay_min:x_overlay_max, 3] / (1.0 * (255.0 * transparency)) # * transparency
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        background[y_background_min:y_background_max, x_background_min:x_background_max, c] = (
            alpha_s * overlay[y_overlay_min:y_overlay_max, x_overlay_min:x_overlay_max, c] + 
            alpha_l * background[y_background_min:y_background_max, x_background_min:x_background_max, c])

    return background

 
if __name__ == '__main__':
    main()
    