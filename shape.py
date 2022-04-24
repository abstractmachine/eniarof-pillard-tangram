import cv2
import depthai
import numpy
import json

# create device pipeline
pipeline = depthai.Pipeline()

shapeData = None
roiJson = None
focus = 127
roiBox = (100,300,50,200)
roiColor = (255,0,255)

with open('shape.json') as shape_json:
	shapeData = json.load(shape_json)
	roiBox = (shapeData["roiBox"][0], shapeData["roiBox"][1], shapeData["roiBox"][2], shapeData["roiBox"][3])
	focus = shapeData["focus"]

windowDimensions = (720,405)
mouseIsPressed = False

# define sources
camera = pipeline.create(depthai.node.ColorCamera)

edgeDetector = pipeline.create(depthai.node.EdgeDetector)
sobelA = 1
sobelB = 2
sobelHorizontalKernel = [[-sobelA,0,sobelA], [-sobelB,0,sobelB], [-sobelA,0,sobelA]]
sobelVerticalKernel = [[-sobelA,-sobelB,-sobelA], [0,0,0], [sobelA,sobelB,sobelA]]
edgeDetector.initialConfig.setSobelFilterKernels(sobelHorizontalKernel, sobelVerticalKernel)
xoutEdge = pipeline.create(depthai.node.XLinkOut)
xoutEdge.setStreamName("edge")
xinEdge = pipeline.create(depthai.node.XLinkIn)
xinEdge.setStreamName("edge config")

# properties
camera.setBoardSocket(depthai.CameraBoardSocket.RGB)
camera.setResolution(depthai.ColorCameraProperties.SensorResolution.THE_1080_P)
camera.initialControl.setAutoFocusMode(depthai.CameraControl.AutoFocusMode.OFF)
camera.initialControl.setManualFocus(focus)

edgeDetector.setMaxOutputFrameSize(camera.getVideoWidth() * camera.getVideoHeight())

# link
camera.video.link(edgeDetector.inputImage)
edgeDetector.outputImage.link(xoutEdge.input)
xinEdge.out.link(edgeDetector.inputConfig)

def mouseCallback(event, x, y, flags, param) :

	global mouseIsPressed, roiBox

	x = int(x * camera.getVideoWidth() / 720)
	y = int(y * camera.getVideoHeight() / 405)

	if event == cv2.EVENT_LBUTTONDOWN:
		mouseIsPressed = True
		roiBox = (x,y,roiBox[2],roiBox[3])
	elif event == cv2.EVENT_MOUSEMOVE:
		if mouseIsPressed:
			roiBox = (roiBox[0],roiBox[1],x-roiBox[0],y-roiBox[1])
	elif event == cv2.EVENT_LBUTTONUP:
		mouseIsPressed = False
		if x > roiBox[0] and y > roiBox[1]:
			roiBox = (roiBox[0],roiBox[1],x-roiBox[0],y-roiBox[1])
			with open('shape.json', 'w') as shape_json:
				shapeData["roiBox"][0] = roiBox[0]
				shapeData["roiBox"][1] = roiBox[1]
				shapeData["roiBox"][2] = roiBox[2]
				shapeData["roiBox"][3] = roiBox[3]
				json.dump(shapeData, shape_json)

cv2.namedWindow("edge")
cv2.setMouseCallback("edge", mouseCallback)

# initialize device
with depthai.Device(pipeline) as device:

    edgeQueue = device.getOutputQueue("edge")
    edgeConfigQueue = device.getInputQueue("edge config")

    while(True):
        edgeCamera = edgeQueue.get()
        edgeFrame = edgeCamera.getFrame()

        cv2.rectangle(edgeFrame, (roiBox[0],roiBox[1],roiBox[2],roiBox[3]), roiColor, 2)

        cv2.namedWindow("edge", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("edge", 720, 405)
        edgeResize = cv2.resize(edgeFrame, (720,405) )
        cv2.imshow("edge", edgeResize)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break
