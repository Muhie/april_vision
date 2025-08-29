from april_vision import Processor, USBCamera, calibrations, find_cameras
from april_vision.examples.camera import setup_cameras

import cv2

# print(calibrations)

# tag_sizes = {
#     range(0, 100): 10
# }

# cameras = setup_cameras(tag_sizes)


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
    tag_sizes=0.01,
    calibration=source.calibration
)






cap = cv2.VideoCapture(0)



while True:
    # feed, ret = cap.read()
    # cv2.imshow("b", ret)
    frames, labels = cam.return_frames()

    # if colour:
    #         output_frame = frame.colour_frame
    #     else:
    #         output_frame = frame.grey_frame
    # try:
    b = cv2.line(frames.colour_frame, [0,20], [20, 40], thickness=10, color = (0, 255, 0))
    cv2.imshow("b", b)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # except:
    #     pass
    # file = cam.save("test")
    # for marker in markers:
    #     print(marker.id)
    # print(markers)

