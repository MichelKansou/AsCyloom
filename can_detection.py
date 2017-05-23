# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import smbus
import cv2

def isset(v):
    try:
        type(eval(v))
    except BaseException:
        return 0
    else:
        return 1

# cascade directory
cascPath = './resources/cascade_5.xml'
cokeCascade = cv2.CascadeClassifier(cascPath)

# I2C Raspberry
bus = smbus.SMBus(1)
address = 0x12

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))


# initialize IA
searching = True
goToBase = False


# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(
        rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
    image = frame.array
    if searching:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cokes = cokeCascade.detectMultiScale(gray, 2, 25)
        # If a can of coke was found
        if isset('cokes'):
            # Draw a rectangle around the cokes
            for (x, y, w, h) in cokes:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                bx = x + w
                by = y + h
                ox = (x + bx)/2
                oy = (y + by)/2
                print("A :(%d, %d)" % (x, y))
                if (ox > 280 and ox < 360):
                    print("Center")
                    print ("Send Move Forward")
                    bus.write_byte(address, 1)
                if ox > 360:
                    print("Right")
                    print("Send Move to Right")
                    bus.write_byte(address, 4)
                if ox < 280:
                    print("Left")
                    print("Send Move to Left")
                    bus.write_byte(address, 3)
                print("Central pos: (%d, %d)" % (ox, oy))
    if goToBase:
        print("Going to base sir")
    else:
        print("[Warning]Target lost...")

    # show the frame
    cv2.imshow("Tracking", image)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
       break
