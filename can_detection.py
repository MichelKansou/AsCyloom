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
targetLost = 0
direction = 0
objectDetected = 0

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(
        rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
    image = frame.array
    #if (searching == True and goToBase == False):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cokes = cokeCascade.detectMultiScale(gray, 2, 25)
    # If a can of coke was found
    print (isset('cokes'))
    if isset('cokes'):
        print("Object Detected")
        #if objectDetected != 1:
           # objectDetected = 1
           # bus.write_byte(address, 11)
        # Draw a rectangle around the cokes
        for (x, y, w, h) in cokes:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            bx = x + w
            by = y + h
            ox = (x + bx)/2
            oy = (y + by)/2
            print("Target  position: (%d, %d)" % (ox, oy))
    else:
        print("[Warning]Target lost...")
        #targetLost += 1
        #if objectDetected != 0:
            #objectDetected = 0
            #bus.write_byte(address, 12)
            #    if (ox > 280 and ox < 360):
            #        print("Center")
            #        print ("Send Move Forward")
            #        if direction != 1:
            #            direction = 1
                        #bus.write_byte(address, 1)
            #    elif ox > 360:
            #        print("Right")
            #        print("Send Move to Right")
            #        if direction != 4:
            #            direction = 4
            #            bus.write_byte(address, 4)
            #    elif ox < 280:
            #        print("Left")
            #        print("Send Move to Left")
            #        if direction !=3:
            #            direction = 3
            #            bus.write_byte(address, 3)
#    if (goToBase == True and searching == False):
#        targetLost = 0
#        print("Going to base sir")
#    if (targetLost > 20 and direction != 0):
#        print("Stop")
#        direction = 0
#        bus.write_byte(address, 0)
    # show the frame
    cv2.imshow("Tracking", image)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
       break
