import sys
sys.path.append('/usr/lib/python3/dist-packages')

from picamera2 import Picamera2
import cv2
import numpy as np
import matplotlib.pyplot as plt
import time

picam2 = Picamera2()
picam2.start()

print("Recording... Press 'q' to stop and plot.")

values = []
start = time.time()

while True:
    frame = picam2.capture_array()

    # Compute mean green intensity
    green_mean = np.mean(frame[:, :, 1])
    values.append(green_mean)

    cv2.imshow("Camera Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
picam2.stop()

# Plot after quitting
plt.plot(values)
plt.title("Green Intensity Over Time")
plt.xlabel("Frame")
plt.ylabel("Mean Green Intensity")
plt.show()
