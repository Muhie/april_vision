from april_vision import Processor, USBCamera, calibrations, find_cameras
from april_vision.examples.camera import setup_cameras
import numpy as np
import cv2
from skimage import morphology, graph
from skan import Skeleton
import math
import pandas as pd
from pandas import DataFrame

### PARAMETERS TO CHANGE DEPENDING ON YOUR TEST RIG

distance_between_markers_0_3 = 605 # distance in mm 
distance_between_markers_0_1 = 190 # distance in mm
distance_between_marker_0_eversion_robot = 300 # distance in mm

cameras = find_cameras(calibrations)

print(cameras)

try:
    camera = cameras[0]
except IndexError:
    print("No cameras found")
    exit()

source = USBCamera.from_calibration_file(
    camera.index,
    camera.calibration,
    camera.vidpid
)

cam = Processor(
    source,
    tag_family='tag36h11',
    quad_decimate=2.0,
    tag_sizes=0.035,
    calibration=source.calibration
)






cap = cv2.VideoCapture(0)





def write_to_csv(x_distance, y_distance, distan):
    a = pd.DataFrame([[abs(x_distance - distance_between_marker_0_eversion_robot), y_distance]],
                        columns=['x', 'y'])
    a.to_csv('april_vision/data.csv', mode='a', index=False, header=False)

while True:
    frames, test, labels  = cam.return_frames()
    b = frames.colour_frame
    b = cv2.line(frames.colour_frame, labels[2], labels[0], thickness=10, color = (0, 255, 0))
    b = cv2.line(b, labels[2], labels[4], thickness=10, color = (0, 255, 0))
    b = cv2.line(b, labels[4], labels[6], thickness=10, color = (0, 255, 0))
    b = cv2.line(b, labels[0], labels[6], thickness=10, color = (0, 255, 0))

    
    img_hsv=cv2.cvtColor(b, cv2.COLOR_BGR2HSV)

    # lower mask (0-10)
    lower_red = np.array([0,50,50])
    upper_red = np.array([10,255,255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

    # upper mask (170-180)
    lower_red = np.array([170,50,50])
    upper_red = np.array([180,255,255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

    # join masks toghte
    mask = mask0+mask1



    blur = cv2.blur(mask,(5,5))
    blurred = cv2.GaussianBlur(blur, (255, 255), 0)
    ret, thresh = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY)
    # skeletonize image and split skeleton to paths
    skeleton = morphology.skeletonize(thresh, method='lee')
    g = Skeleton(skeleton)
    path = np.array(g.path_coordinates(0).astype(int))

    points_list = []
    for p in path:
        cv2.drawMarker(b, (p[1], p[0]),(0,0,255), markerType=cv2.MARKER_STAR, 
        markerSize=10, thickness=2, line_type=cv2.LINE_AA)
        points_list.append(p)

    total_angle = 0




    x_end = path[0][0]
    y_end = path[0][1]
    x_start = path[len(path)-1][0]
    y_start = path[len(path)-1][1]

    length_of_one_pixel_in_mm_x = (distance_between_markers_0_3 / math.sqrt((labels[6][0] - labels[0][0])**2 + (labels[6][1] - labels[0][1]) **2))
    length_of_one_pixel_in_mm_y = (distance_between_markers_0_1 / math.sqrt((labels[2][0] - labels[0][0])**2 + (labels[2][1] - labels[0][1]) **2))

    x_distance = abs(labels[0][0] - y_end) * length_of_one_pixel_in_mm_x
    y_distance = abs(labels[0][1] - x_end) * length_of_one_pixel_in_mm_y

    # b = cv2.line(b, (labels[0][0], x_end), (y_end, x_end), thickness=10, color = (255, 0, 0))
    b = cv2.line(b, (labels[0][0], x_end), (labels[0][0], x_end), thickness=10, color = (255, 0, 0))

    b = cv2.line(b, labels[0], (y_end, x_end), thickness=10, color = (255, 0, 0))
    b = cv2.line(b, labels[0], (y_start, x_start), thickness=10, color = (255, 0, 0))




    x_text = "X: {}".format(x_distance)
    cv2.putText(
        img = b,
        text = x_text,
        org = (0, 50),
        fontFace = cv2.FONT_HERSHEY_DUPLEX,
        fontScale = 1.5,
        color = (125, 246, 55),
        thickness = 2
    )
    y_text = "Y: {}".format(y_distance)
    cv2.putText(
        img = b,
        text = y_text,
        org = (0, 100),
        fontFace = cv2.FONT_HERSHEY_DUPLEX,
        fontScale = 1.5,
        color = (125, 246, 55),
        thickness = 2
    )
    write_to_csv(x_distance, y_distance, distance_between_marker_0_eversion_robot)
    cv2.imshow("Video Feed", b)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

