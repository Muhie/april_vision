"""An AprilTags wrapper with camera discovery and axis conversion."""
# ruff: noqa: E402
import os

os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

from .calibrations import calibrations
from .detect_cameras import CalibratedCamera, find_cameras
from .frame_sources import FrameSource, USBCamera
from .helpers import generate_marker_size_mapping
from .marker import (
    CartesianCoordinates,
    Marker,
    Orientation,
    PixelCoordinates,
    SphericalCoordinate,
)
from .utils import Frame
from .vision import Processor

__all__ = [
    'CalibratedCamera',
    'CartesianCoordinates',
    'Frame',
    'FrameSource',
    'Marker',
    'Orientation',
    'PixelCoordinates',
    'Processor',
    'SphericalCoordinate',
    'USBCamera',
    '0.1.0',
    'calibrations',
    'find_cameras',
    'generate_marker_size_mapping',
]
