from april_vision.examples.camera import setup_cameras

# Markers 0-100 are 80mm in size
tag_sizes = {
    range(0, 255): 100
}

# Returns a dict of index and camera
cameras = setup_cameras(tag_sizes)

if len(cameras) == 0:
    print("No cameras found")

for serial, cam in cameras.items():
    print(cam.model, serial)
    print(cam.see())