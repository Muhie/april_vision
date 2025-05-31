from april_vision import Processor, USBCamera, calibrations, find_cameras


print(calibrations)

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
    tag_sizes=0.08,
    calibration=source.calibration
)


print("yea")
while True:
    markers = cam.see()
    for marker in markers:
        print(marker.id)
    print(markers)