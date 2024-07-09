import keyboard
import time
import serial
import pygame

pygame.init()
pygame.display.set_mode((400, 800))
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


# # Initialize your serial connection here
# arduino = serial.Serial('/dev/ttyACM0', 9600)  # replace '/dev/ttyACM0' with your port

# current_servo = 0

# def change_angle():
#     while True:
#         if keyboard.is_pressed('up'):
#             # Increase the angle of the current servo
#             arduino.write((str(current_servo) + 'u').encode())  # send command to Arduino
#             time.sleep(0.01)  # add delay as needed
#         elif keyboard.is_pressed('down'):
#             # Decrease the angle of the current servo
#             arduino.write((str(current_servo) + 'd').encode())  # send command to Arduino
#             time.sleep(0.01)  # add delay as needed

# def select_servo(e):
#     # Select the servo corresponding to the number key pressed
#     global current_servo
#     current_servo = int(e.name) - 1

# # Bind the number keys to the select_servo function
# for i in range(1, 7):
#     keyboard.on_press_key(str(i), select_servo)

# # Start the loop to change angle
# change_angle()
