import pygame
import sys
import serial
import time

pygame.init()
screen = pygame.display.set_mode((400, 400))
font = pygame.font.Font(None, 40)

# initialize serial connection to Arduino
arduino = serial.Serial('COM4', 9600)

class RoboticArm:
    def __init__(self):
        self.angles = [0, 0, 0, 0, 0, 140]  # initialize servo degrees
        self.motor = 0
        self.last_update_time = pygame.time.get_ticks()
        self.motor_speed = {"SLOW": 20, "FAST": 5}
        self.motor_speed_indices = {0: "SLOW", 1: "FAST"}
        self.motor_speed_val = 0

    def handle_keypress(self, keys):
        if keys[pygame.K_UP]: self.motor_speed_val = 1
        if keys[pygame.K_DOWN]: self.motor_speed_val = 0

        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.motor_speed.get(self.motor_speed_indices.get(self.motor_speed_val)):
            if keys[pygame.K_RIGHT]:
                if self.motor == 5 and self.angles[self.motor] < 140:
                    self.angles[self.motor] += 1
                elif self.motor != 5 and self.angles[self.motor] < 179:
                    self.angles[self.motor] += 1
                command = f"<{self.motor}:{self.angles[self.motor]}>"
                arduino.write(command.encode())  # send motor and angle as "<motor:angle>"
                print(f"Sent: {command}")
                
            elif keys[pygame.K_LEFT]:
                if self.motor == 5 and self.angles[self.motor] > 75:
                    self.angles[self.motor] -= 1
                elif self.motor != 5 and self.angles[self.motor] > 1:
                    self.angles[self.motor] -= 1
                command = f"<{self.motor}:{self.angles[self.motor]}>"
                arduino.write(command.encode())
                print(f"Sent: {command}")
                
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
    arm.display_angles(screen)
    arm.display_speed(screen)

    header = font.render("Robotic Arm Controller", True, (0, 0, 0))
    header_rect = header.get_rect(center=(150, 25))
    pygame.draw.rect(screen, (252, 173, 3), (0, 0, 400, 50))
    screen.blit(header, (45, 13))
    pygame.draw.line(screen, (196, 135, 4), (0, 50), (400, 50), 4)

    pygame.display.flip()

    # debugging
    if arduino.in_waiting > 0:
        data = arduino.readline().decode(errors='ignore').strip()
        print(f"Received from Arduino: {data}")

    clock.tick(60)
