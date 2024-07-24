import keyboard
import time
import serial
import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((400, 400))
font = pygame.font.Font(None, 40)

class RoboticArm:
    def __init__(self):
        self.angles = [0, 0, 0, 0, 0, 0]
        self.motor = 0
        self.last_update_time = pygame.time.get_ticks()
        self.motor_speed = {"SLOW": 20, "FAST": 5}
        self.motor_speed_indices = {0: "SLOW", 1: "FAST"}
        self.motor_speed_val = 0

    def draw(self, screen):
        # if I want to draw arm on the screen
        pass

    def handle_keypress(self, keys):
        
        if keys[pygame.K_UP]: self.motor_speed_val = 1
        if keys[pygame.K_DOWN]: self.motor_speed_val = 0

        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.motor_speed.get(self.motor_speed_indices.get(self.motor_speed_val)):
            if keys[pygame.K_RIGHT] and self.angles[self.motor] < 179: self.angles[self.motor] += 1
            elif keys[pygame.K_LEFT] and self.angles[self.motor] > 1: self.angles[self.motor] -= 1
            elif keys[pygame.K_1]: self.motor = 0
            elif keys[pygame.K_2]: self.motor = 1
            elif keys[pygame.K_3]: self.motor = 2
            elif keys[pygame.K_4]: self.motor = 3
            elif keys[pygame.K_5]: self.motor = 4
            elif keys[pygame.K_6]: self.motor = 5

            self.last_update_time = current_time

    def display_angles(self, screen):
        for i, angle in enumerate(self.angles):
            text = font.render(f"Motor {i + 1}: {angle} degrees", True, (0, 0, 0))
            screen.blit(text, (120, i * 40 + 60))
            
    def display_speed(self, screen):
        text = font.render(f"Speed: {self.motor_speed_indices.get(self.motor_speed_val)}", True, (0, 0, 0))
        screen.blit(text, (120, 360))


arm = RoboticArm()
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    keys = pygame.key.get_pressed()
    arm.handle_keypress(keys)

    screen.fill((255, 255, 255))
    # arm.draw(screen)
    arm.display_angles(screen)
    arm.display_speed(screen)

    header = font.render("Robotic Arm Controller", True, (0, 0, 0))
    header_rect = header.get_rect(center=(150, 25))
    pygame.draw.rect(screen, (252, 173, 3), (0, 0, 400, 50))
    screen.blit(header, (45, 13))
    pygame.draw.line(screen, (196, 135, 4), (0, 50), (400, 50), 4)

    pygame.display.flip()

    clock.tick(60)


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
