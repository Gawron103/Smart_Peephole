class FPSMeter:
    def __init__(self):
        self.newFrameTime = 0
        self.prevFrameTime = 0

    def calculateFPS(self, frameTime):
        self.newFrameTime = frameTime
        fps = 1 / (self.newFrameTime - self.prevFrameTime)
        self.prevFrameTime = self.newFrameTime
        return str(int(fps))