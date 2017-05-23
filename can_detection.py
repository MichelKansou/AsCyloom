# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import imutils
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

# define the lower and upper boundaries for extraction point
# define the list of boundaries
lower = (0, 100, 100)
upper = (179, 250, 250)


# initialize IA
searching = False
goToBase = True
targetLost = 0
direction = 0
objectDetected = 0
ColorDetectionImage = 0

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(
        rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
    image = frame.array
    print("Object Distance : %d" % bus.read_byte(address))
    if (searching == True and goToBase == False):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cokes = cokeCascade.detectMultiScale(gray, 2, 25)
        # If a can of coke was found
        if len(cokes) > 0:
            targetLost = 0
            if objectDetected != 1:
                 objectDetected = 1
                 bus.write_byte(address, 11)
            # Draw a rectangle around the cokes
            for (x, y, w, h) in cokes:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                bx = x + w
                by = y + h
                ox = (x + bx)/2
                oy = (y + by)/2
                if (ox > 290 and ox < 350):
                   print("Center")
                   print ("Send Move Forward")
                   if direction != 1:
                       direction = 1
                   bus.write_byte(address, 0)
                   if bus.read_byte(address) < 10:
                       bus.write_byte(address, 0)
                   else:
                       bus.write_byte(address, 1)
                elif ox > 350:
                   print("Right")
                   print("Send Move to Right")
                   if direction != 4:
                       direction = 4
                       bus.write_byte(address, 4)
                elif ox < 290:
                   print("Left")
                   print("Send Move to Left")
                   if direction !=3:
                       direction = 3
                       bus.write_byte(address, 3)
                print("Target  position: (%d, %d)" % (ox, oy))
        else:
           targetLost += 1
           if objectDetected != 0:
              objectDetected = 0
              bus.write_byte(address, 12)
              print("[Warning]Target lost...")
    if (goToBase == True and searching == False):
        image = imutils.resize(image, width=600)
        blurred = cv2.GaussianBlur(image, (11, 11), 0)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, lower, upper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        ColorDetectionImage = mask.copy()

        # find contours in the mask image
        contours = cv2.findContours(ColorDetectionImage, cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # finding contour with maximum area and store it as best_cnt
        max_area = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > max_area:
                max_area = area
                best_cnt = cnt
        # finding centroids of best_cnt and draw a circle there
        if isset('best_cnt'):
            targetLost = 0
            print("Going to base sir")
            M = cv2.moments(best_cnt)
            cx, cy = int(M['m10'] / M['m00']), int(M['m01'] / M['m00'])
            cv2.rectangle(image, (cx, cy), (cx + 10, cy + 20), (255, 255, 0), 2)
            print("Base Position: (%d, %d)" % (cx, cy))
    if (targetLost > 5 and direction != 0):
        print("Stop")
        direction = 0
        bus.write_byte(address, 0)
        if (bus.read_byte(address) < 10):
            bus.write_byte(address, 2)
            time.sleep(0.5)
            bus.write_byte(address, 4)
        else:
            bus.write_byte(address, 4)
    # show the frame
    cv2.imshow("Tracking", image)
    if (len(ColorDetectionImage) > 0):
        cv2.imshow("Infra", ColorDetectionImage)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
       break
