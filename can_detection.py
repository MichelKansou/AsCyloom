# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

def isset(v):
    try:
        type(eval(v))
    except BaseException:
        return 0
    else:
        return 1

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
    mask = cokes.copy()

    # find contours in the mask image
    contours = cv2.findContours(mask, cv2.RETR_EXTERNAL,
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
        M = cv2.moments(best_cnt)
        cx, cy = int(M['m10'] / M['m00']), int(M['m01'] / M['m00'])
        cv2.rectangle(image, (cx, cy), (0, 255, 0), 2)
        # cv2.circle(image, (cx, cy), 5, 255, -1)
        print("Central pos: (%d, %d)" % (cx, cy))
    else:
        print("[Warning]no Taget Found...")

    # Draw a rectangle around the faces
    # for (x, y, w, h) in cokes:
    #     cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # show the frame
    cv2.imshow("Tracking", image)
    cv2.imshow("thresh", mask)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
       break
