"""
RC for Tello Drone with camera feed
Author: Charles Lee
"""

import pygame
from pygame.locals import *
import sys
import time
from rktellolib import Tello

# Setup Pygame Window
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 720
FRAMES_PER_SECOND = 30
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Setup Tello drone
drone = Tello(debug=True, has_video=True)
drone.connect()

# Ends Pygame
def cleanup():
    drone.land()
    drone.disconnect()
    time.sleep(1)
    pygame.quit()
    sys.exit()

# RC Control Inputs
lr = 0
fb = 0
ud = 0
yaw = 0
speed = 100

try:
    drone.rc(0,0,0,0)
    drone.takeoff()

    while True:
        # Handle keyboard events
        for event in pygame.event.get():
            if (event.type == QUIT) or ((event.type == KEYDOWN) and (event.key == K_ESCAPE)):
                cleanup()
        
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    lr = -speed
                elif event.key == pygame.K_d:
                    lr = speed
                if event.key == pygame.K_w:
                    fb = speed
                elif event.key == pygame.K_s:
                    fb = -speed
                if event.key == pygame.K_q:
                    yaw = -speed
                elif event.key == pygame.K_e:
                    yaw = speed
                elif event.key == pygame.K_r:
                    ud = speed
                elif event.key == pygame.K_f:
                    ud = -speed
                drone.rc(lr, fb, ud, yaw)
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_a, pygame.K_d):
                    lr = 0
                if event.key in (pygame.K_w, pygame.K_s):
                    fb = 0
                if event.key in (pygame.K_q, pygame.K_e):
                    yaw = 0
                if event.key in (pygame.K_r, pygame.K_f):
                    ud = 0
                drone.rc(lr, fb, ud, yaw)
                
        # Show video feed
        frame = drone.get_frame()
        if frame is not None:
            img = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "BGR")
            window.blit(img, (0,0))

        pygame.display.update()
        clock.tick(FRAMES_PER_SECOND)
except:
    cleanup()