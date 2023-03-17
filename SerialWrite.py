import serial
import time
import sys
import tty
import termios

# Set up the serial port connection
ser = serial.Serial('/dev/ttyACM0', 57600, timeout=1)

# Define a function to get a single character from the keyboard
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# Start the keyboard listener
while True:
    # Get a single character from the keyboard
    key = getch()

    # Check if cursor keys are pressed and generate X and Y values accordingly
    x = 0
    y = 0
    if key == 'w':  # up arrow
        x = 100
        y = 100
    elif key == 's':  # down arrow
        x = -100
        y = -100
    elif key == 'd':  # right arrow
        x = 100
        y = -100
    elif key == 'a':  # left arrow
        x = -100
        y = 100

    # Check if 's' key is pressed to stop the robot
    if key == 'p':
        x = 0
        y = 0

    # Format the 'm' command with the X and Y values
    command = 'm {} {}\r'.format(x, y)

    # Send the command to the serial port
    ser.write(command.encode())

    # Wait for a short time before sending the next command
    time.sleep(0.1)

