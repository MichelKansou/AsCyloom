# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2


# cascade directory
cascPath = './resources/cascade_2.xml'
cokeCascade = cv2.CascadeClassifier(cascPath)

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(
        rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
    image = frame.array

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cokes = cokeCascade.detectMultiScale(gray, 2, 10)

    # Draw a rectangle around the faces
    for (x, y, w, h) in cokes:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # show the frame
    cv2.imshow("Tracking", image)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
       break
