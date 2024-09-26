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
        self.angles = [0, 0, 0, 180, 180, 140]  # initialize servo degrees
        self.motor = 0
        self.target_angles = self.angles.copy()
        self.last_update_time = pygame.time.get_ticks()
        self.motor_speed = {"SLOW": 20, "FAST": 5}
        self.motor_speed_indices = {0: "SLOW", 1: "FAST"}
        self.motor_speed_val = 0
        self.command_interval = 100  # milliseconds
        self.last_command_time = pygame.time.get_ticks()

    def handle_keypress(self, keys):
        if keys[pygame.K_UP]: self.motor_speed_val = 1
        if keys[pygame.K_DOWN]: self.motor_speed_val = 0

        current_time = pygame.time.get_ticks()
        
        if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
            if current_time - self.last_command_time > self.command_interval:
                increment = 5 if keys[pygame.K_RIGHT] else -5
                if self.motor == 5 and (self.target_angles[self.motor] < 140 and increment > 0 or self.target_angles[self.motor] > 75 and increment < 0):
                    self.target_angles[self.motor] += increment
                elif self.motor != 5 and (self.target_angles[self.motor] < 179 and increment > 0 or self.target_angles[self.motor] > 1 and increment < 0):
                    self.target_angles[self.motor] += increment
                
                command = f"<{self.motor}:{self.target_angles[self.motor]}>"
                arduino.write(command.encode())
                print(f"Sent: {command}")
                self.last_command_time = current_time
        
        # servo selection
        for i in range(6):
            if keys[pygame.K_1 + i]:
                self.motor = i

        # smooth transition
        for i in range(6):
            if self.angles[i] != self.target_angles[i]:
                if self.angles[i] < self.target_angles[i]:
                    self.angles[i] += 1
                elif self.angles[i] > self.target_angles[i]:
                    self.angles[i] -= 1

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

    # Debugging
    if arduino.in_waiting > 0:
        data = arduino.readline().decode(errors='ignore').strip()
        print(f"Received from Arduino: {data}")

    clock.tick(60)
