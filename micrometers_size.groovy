def server = getCurrentServer()
def cal = server.getPixelCalibration()
print cal.getPixelWidthMicrons()
print cal.getPixelHeightMicrons()
print cal.getAveragedPixelSizeMicrons()