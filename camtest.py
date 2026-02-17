import sys
sys.path.append('/usr/lib/python3/dist-packages')  # Picamera2 lives here
from picamera2 import Picamera2
from picamera2 import Picamera2
import cv2

picam2 = Picamera2()
picam2.start()

print("Camera running. Press 'q' to quit.")

while True:
    frame = picam2.capture_array()  # numpy array
    cv2.imshow("Camera Test", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
picam2.stop()
