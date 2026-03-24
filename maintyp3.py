from april_vision import Processor, USBCamera, calibrations, find_cameras
from april_vision.examples.camera import setup_cameras
import numpy as np
import cv2
import math
import pandas as pd
from pandas import DataFrame

### PARAMETERS TO CHANGE DEPENDING ON YOUR TEST RIG

distance_between_markers_0_3 = 500 # distance in mm 
distance_between_markers_0_1 = 500 # distance in mm
distance_between_marker_0_eversion_robot = 250 # distance in mm
distance_from_wall_to_mount = 0 # distance in mm

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
    tag_sizes=0.055,
    calibration=source.calibration
)






cap = cv2.VideoCapture(0)

# Ask for filename to save data
filename = input("Enter filename for data (without .csv extension): ").strip()
if not filename:
    filename = "data"
csv_filename = f"testdata/{filename}.csv"

# Create/initialize the CSV file with headers
headers_df = pd.DataFrame(columns=['x', 'y'])
headers_df.to_csv(csv_filename, index=False)

def write_to_csv(x_distance, y_distance):
    a = pd.DataFrame([[x_distance, y_distance]],
                        columns=['x', 'y'])
    a.to_csv(csv_filename, mode='a', index=False, header=False)

while True:
    frames, test, labels  = cam.return_frames()
    b = frames.colour_frame
    # b = cv2.line(frames.colour_frame, labels[2], labels[0], thickness=10, color = (0, 255, 0))
    # b = cv2.line(b, labels[2], labels[4], thickness=10, color = (0, 255, 0))
    # b = cv2.line(b, labels[4], labels[6], thickness=10, color = (0, 255, 0))
    # b = cv2.line(b, labels[0], labels[2], thickness=10, color = (0, 255, 0))

    
    img_hsv=cv2.cvtColor(b, cv2.COLOR_BGR2HSV)

    # lower mask (0-5) - pure red only
    lower_red = np.array([0,150,100])
    upper_red = np.array([5,255,255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

    # upper mask (175-180) - pure red only
    lower_red = np.array([175,150,100])
    upper_red = np.array([180,255,255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

    # join masks together
    mask = mask0+mask1



    blur = cv2.blur(mask,(5,5))
    blurred = cv2.GaussianBlur(blur, (5, 5), 0)
    ret, thresh = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY)
    
    # Find contours to detect the red dot
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    dot_center_x = None
    dot_center_y = None
    
    # Filter contours by minimum area (20x20 = 400 pixels)
    min_area = 25 * 25
    valid_contours = [c for c in contours if cv2.contourArea(c) >= min_area]
    
    if valid_contours:
        # Find the largest contour (the red dot)
        largest_contour = max(valid_contours, key=cv2.contourArea)
        
        # Calculate the centroid of the dot
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            dot_center_x = int(M["m10"] / M["m00"])
            dot_center_y = int(M["m01"] / M["m00"])
            
            # Draw the dot center on the frame
            cv2.drawMarker(b, (dot_center_x, dot_center_y), (0, 0, 255), 
                          markerType=cv2.MARKER_CROSS, markerSize=15, thickness=2)
            cv2.circle(b, (dot_center_x, dot_center_y), 5, (0, 255, 255), -1)

    length_of_one_pixel_in_mm_x = (distance_between_markers_0_3 / math.sqrt((labels[2][0] - labels[0][0])**2 + (labels[2][1] - labels[0][1]) **2))    
    length_of_one_pixel_in_mm_y = (distance_between_markers_0_3 / math.sqrt((labels[2][0] - labels[0][0])**2 + (labels[2][1] - labels[0][1]) **2))

    # Calculate distance from April tag to red dot center
    if dot_center_x is not None and dot_center_y is not None:
        x_distance = (labels[0][0] - dot_center_x) * length_of_one_pixel_in_mm_x
        y_distance = (labels[0][1] - dot_center_y) * length_of_one_pixel_in_mm_y
        x_raw = (labels[0][0] - dot_center_x) * length_of_one_pixel_in_mm_x
        y_raw = (labels[0][1] - dot_center_y) * length_of_one_pixel_in_mm_y
        
        # Draw line from April tag to red dot
        b = cv2.line(b, tuple(labels[0]), (dot_center_x, dot_center_y), thickness=2, color=(255, 0, 0))
    else:
        x_distance = 0
        y_distance = 0
        x_raw = 0
        y_raw = 0




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
    write_to_csv(x_distance, y_distance)
    cv2.imshow("Video Feed", b)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

