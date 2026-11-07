import serial
import time

from tenacity import sleep

# Initialize Serial Communication
# CHANGE 'COM3' TO YOUR ACTUAL ARDUINO PORT (e.g., 'COM5', '/dev/ttyACM0')
try:
    arduino = serial.Serial(port='COM6', baudrate=9600, timeout=1)
    # Give the Arduino 2 seconds to reset after opening the serial port
    time.sleep(2)
    print("Successfully connected to Arduino.")
except Exception as e:
    print(f"Error connecting to Arduino: {e}")
    exit()

start = [0, 0, 0]


def send_data(vals):
    """Formats the list into a comma-separated string and sends it to Arduino."""
    # Converts [90, 180, 90] into "90,180,90\n"
    data_str = f"{vals[0]},{vals[1]},{vals[2]}\n"
    arduino.write(data_str.encode('utf-8'))


def move(target, delay=0.01):
    """Moves the servos smoothly step-by-step to the target position."""
    global start

    # Find the maximum difference to determine how many steps we need
    max_steps = max(abs(target[i] - start[i]) for i in range(3))

    if max_steps == 0:
        return

    # Gradually step towards the target
    for step in range(1, max_steps + 1):
        current = [0, 0, 0]
        for i in range(3):
            if start[i] < target[i]:
                current[i] = min(start[i] + step, target[i])
            else:
                current[i] = max(start[i] - step, target[i])

        send_data(current)
        time.sleep(delay)

    # Update the start position for the next movement
    start = target[:]


def hello():
    global start
    print("Waving...")
    # Wave the middle servo (index 1)
    move([start[0], 180, start[2]])
    for _ in range(3):
        move([start[0], 150, start[2]])
        move([start[0], 180, start[2]])
    move([start[0], 0, start[2]])
    print("Done waving.")


# Set initial target
time.sleep(1)
target = [0, 0, 0]
move(target)




# Execute the hello sequence


# Close the serial port when done
arduino.close()

