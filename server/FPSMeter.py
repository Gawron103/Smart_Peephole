class FPSMeter:
    def __init__(self):
        self.__newFrameTime = 0
        self.__prevFrameTime = 0

    def calculate_fps(self, frame_time):
        self.__newFrameTime = frame_time
        fps = 1 / (self.__newFrameTime - self.__prevFrameTime)
        self.__prevFrameTime = self.__newFrameTime
        return str(int(fps))
