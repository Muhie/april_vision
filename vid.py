import cv2
import json
import re
import subprocess


# def default_discovery():
#     """
#     A fallback discovery method for when there is not an OS specific one available.

#     This cannot identify the USB VID & PID of the camera and only provides
#     information on the openable indexes.
#     """
#     found_cameras = []
#     for camera_id in range(8):
#         capture = cv2.VideoCapture(camera_id)
#         if capture.isOpened():
#             print(f"Found camera at index {camera_id}")
#             print(str(camera_id))
#         capture.release()

#     return found_cameras


# default_discovery()


def mac_discovery():
    """
    Discovery method for MacOS using system_profiler.

    This matches camera indexes to their USB VID & PID as long as cameras are
    not attached after cv2 has been imported.
    """
    camera_info = json.loads(
        subprocess.check_output(['system_profiler', '-json', 'SPCameraDataType']),
    )
    camera_list = camera_info["SPCameraDataType"]
    # Preserve devices ordering on the system
    # see AVCaptureDevice::uniqueID property documentation for more info
    # From https://github.com/opencv/opencv/blob/4.11.0/modules/videoio/src/cap_avfoundation_mac.mm#L377
    camera_list.sort(key=lambda x: x["spcamera_unique-id"])
    cameras = []
    print(camera_list)

    for index, camera in enumerate(camera_list):
        try:
            name = camera["_name"]
            camera_data = camera['spcamera_model-id']
            # Use caution, this identifier follows the port not the camera
            unique_id = camera['spcamera_unique-id']

            m = re.search(r'VendorID_([0-9]{1,5}) ProductID_([0-9]{1,5})', camera_data)

            if m is None:
                # Facetime cameras have no PID or VID
                vidpid = camera_data
            else:
                vid = int(m.groups()[0], 10)
                pid = int(m.groups()[1], 10)

                vidpid = f'{vid:04x}:{pid:04x}'

            print(f"Found camera at index {index}: {name}")
            print(index,name,vidpid,unique_id)
            print(vidpid)
        except KeyError:
            print(f"Camera {index} had missing fields: {camera}")


mac_discovery()