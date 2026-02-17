import time
import numpy as np
import matplotlib.pyplot as plt
import max30102

# -----------------------------
# Configuration
# -----------------------------
BUFFER_SIZE = 300
SAMPLE_INTERVAL = 0.05   # seconds per sample
SMOOTH_WINDOW = 2        # smaller smoothing to preserve subtle dips
IR_THRESHOLD = 5000       # counts to detect finger
BASELINE_WINDOW = 50      # last ~2.5 sec used for baseline

# -----------------------------
# Initialize sensor
# -----------------------------
sensor = max30102.MAX30102()
ir_data = []
red_data = []

# -----------------------------
# Setup plot
# -----------------------------
plt.ion()
fig, ax = plt.subplots(figsize=(10, 5))

line_ir, = ax.plot([], [], label="Heartbeat (PPG)", color='blue')
line_red, = ax.plot([], [], label="SpO₂ proxy", color='orange')

ax.set_xlabel("Samples")
ax.set_ylabel("Relative change (counts)")
ax.set_title("MAX30102 Real-Time PPG (Relative Change)")
ax.legend(loc="upper right")

finger_text = ax.text(0.5, 0.5, "Place your finger on the sensor",
                      transform=ax.transAxes, ha='center', va='center',
                      fontsize=14, color='red')

print("Starting relative PPG monitor...")

# -----------------------------
# Main loop
# -----------------------------
while True:
    # Read new sample
    red, ir = sensor.read_fifo()
    ir_data.append(ir)
    red_data.append(red)

    # Keep buffers fixed
    if len(ir_data) > BUFFER_SIZE:
        ir_data.pop(0)
        red_data.pop(0)

    # Finger detection
    if np.mean(ir_data[-10:]) > IR_THRESHOLD:
        finger_text.set_text("")

        ir_array = np.array(ir_data)
        red_array = np.array(red_data)

        # Smooth waveform lightly
        ir_smooth = np.convolve(ir_array, np.ones(SMOOTH_WINDOW)/SMOOTH_WINDOW, mode='same')
        red_smooth = np.convolve(red_array, np.ones(SMOOTH_WINDOW)/SMOOTH_WINDOW, mode='same')

        # Use recent baseline for relative change
        ir_baseline = np.min(ir_smooth[-BASELINE_WINDOW:]) if len(ir_smooth) >= BASELINE_WINDOW else np.min(ir_smooth)
        red_baseline = np.min(red_smooth[-BASELINE_WINDOW:]) if len(red_smooth) >= BASELINE_WINDOW else np.min(red_smooth)

        ir_relative = ir_smooth - ir_baseline
        red_relative = red_smooth - red_baseline

    else:
        # No finger
        finger_text.set_text("Place your finger on the sensor")
        ir_relative = np.zeros(len(ir_data))
        red_relative = np.zeros(len(red_data))

    # Update plot
    line_ir.set_data(range(len(ir_relative)), ir_relative)
    line_red.set_data(range(len(red_relative)), red_relative)

    ax.set_xlim(0, BUFFER_SIZE)
    ax.relim()
    ax.autoscale_view()
    plt.pause(0.01)
