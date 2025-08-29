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
    feed, ret = cap.read()
    cv2.imshow("b", ret)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    markers = cam.see()
    file = cam.save("test")
    for marker in markers:
        print(marker.id)
    print(markers)


capture.release()
cv2.destroyAllWindows()