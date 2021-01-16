from enum import Enum

class CameraState(Enum):
    NEVER_CONNECTED = 0
    CONNECTED = 1
    DISCONNECTED = 2