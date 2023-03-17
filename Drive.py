import serial
import time
import sys
import tty
import termios
import re


# Set up the serial port connection remember to ensure that the arduino motor controller is connccted to the usb port of the raspberry pi
 
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

# Define a function to write the motor speed to the robot
def write_motor_speed(left_motor_speed, right_motor_speed):
    # Format the 'm' command with the left and right motor speeds
    command = 'm {} {}\r'.format(left_motor_speed, right_motor_speed)

    # Send the command to the serial port
    ser.write(command.encode())

    # Wait for a short time before sending the next command
   
    response = ser.readline().decode().strip()
    return response
    

# Define a function to read the encoder positions of each motor
def read_encoder_positions():
    # Send the 'e' command to the serial port
    ser.flushInput() # flush the input buffer
    ser.write('e \r'.encode())
    
    # Read the response from the serial port
    response = ser.readline().decode().strip()

    pattern = r'^-?\d+ -?\d+$'# regex pattern for response with two integers
    match = re.match(pattern, response)
    if match:
        encoder1, encoder2 = map(int, response.split())
        return encoder1, encoder2
    else:
        print(f"Invalid motor response: {response}")
        return None
    

def move_forward(ticks):
    # Get the starting encoder positions of each motor
    start_left, start_right = read_encoder_positions()

    # Calculate the target encoder positions for each motor
    target_left = start_left + ticks
    target_right = start_right + ticks

    # Set the motor speeds to move the robot forward
    motor_speed_left = 30
    motor_speed_right = 30
        

    # Keep moving the robot forward until the target encoder positions are reached
    while True:
        # Calculate the current encoder positions of each motor
        current_left, current_right = read_encoder_positions()

        # Check if the target encoder positions have been reached
        if current_left >= target_left:
            motor_speed_left = 0
        
        if current_right >= target_right:
            motor_speed_right = 0    
        
        if current_left >= target_left and current_right >= target_right:
            break

        write_motor_speed(motor_speed_left, motor_speed_right)

        # Print the current encoder positions
        print('Left position :', current_left)
        print('Right position:', current_right)

        # Wait for a short time before sending the next command
        #time.sleep(0.1)
    # Stop the robot after it has moved forward the desired number of encoder ticks
    write_motor_speed(0, 0)
    print('Robot stopped.')
    return None

# Start the keyboard listener
while True:
    # Get a single character from the keyboard
    key = getch()

    # Check if cursor keys are pressed and generate X and Y values accordingly
    left_motor_speed = 0
    right_motor_speed = 0
    if key == 'w':  # up arrow
        left_motor_speed = 100
        right_motor_speed = 100
    elif key == 's':  # down arrow
        left_motor_speed = -100
        right_motor_speed = -100
    elif key == 'd':  # right arrow
        left_motor_speed = 100
        right_motor_speed = -100
    elif key == 'a':  # left arrow
        left_motor_speed = -100
        right_motor_speed = 100
    elif key == 'p': # Check if 'p' key is pressed to stop the robot
        left_motor_speed = 0
        right_motor_speed = 0
    elif key == 'f': # Check if 'p' key is pressed to stop the robot
        left_motor_speed = 0
        right_motor_speed = 0
        move_forward(1000)
    elif key == 'e': # Check if 'p' key is pressed to stop the robot
        left_position, right_position = read_encoder_positions()
        # Print the encoder positions
        print('Left position :', left_position)
        print('Right position:', right_position)
    elif key == 'x': # Check if 'x' key is pressed to exit the script
        ser.close()
        sys.exit()

    # Write the motor speed to the robot
    write_motor_speed(left_motor_speed, right_motor_speed)

    # Read the encoder positions of each motor
    left_position, right_position = read_encoder_positions()

    # Print the encoder positions
    print('Left position :', left_position)
    print('Right position:', right_position)

    # Wait for a short time before sending the next command
    time.sleep(0.1)



