import pygame
import pygame as pg
import numpy as np
from math import *
from rotations import *
from time import sleep

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
minX, minY, maxX, maxY = -2, 0, 2, 2
Dx, Dy = 0.05, 0.1

WIDTH, HEIGHT = 532, 280
pygame.display.set_caption("3D projection")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

scale = 140

circle_pos = [WIDTH/2, HEIGHT/2]  # x, y
SPEED = 0.05

angleX = 0
angleY = 0
angleZ = 0

points = []

def Bird(x, y) -> np.array:
    x = np.asarray(x)
    y = np.asarray(y)
    return np.absolute(x) * np.absolute(y)

for j in np.arange(minY, maxY, Dy):
    for i in np.arange(minX, maxX, Dx):
        points.append([i, j, Bird(i, j)-1.5])
points = np.array(points)

line_len = int((maxX-minX)/Dx)
downHorizont = points[-line_len:]
upHorizont = points[:line_len]


projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
])

def connect_points(i, j, points):
    pygame.draw.line(
        screen, BLACK, (points[i][0], points[i][1]), (points[j][0], points[j][1]))


clock = pygame.time.Clock()
moving_matrix = [False, False, False, False, False, False]
while True:

    clock.tick(60)

    screen.fill(BLACK)
    # drawining stuff

    rot_z = rotation_z(angleZ)
    rot_y = rotation_y(angleY)
    rot_x = rotation_x(angleX)

    rotated2d = np.dot(points, rot_z)
    rotated2d = np.dot(rotated2d, rot_y)
    rotated2d = np.dot(rotated2d, rot_x)

    projected2d = np.dot(rotated2d, projection_matrix)
    projected2d = np.array(projected2d)

    for i, point in enumerate(projected2d):
        if (projected2d[i%line_len][1] < point[1]):
            x = int(point[0] * scale) + circle_pos[0]
            y = int(point[1] * scale) + circle_pos[1]

            pygame.draw.circle(screen, RED, (x, y-135), 2)
    
    downHorizont2d = np.dot(downHorizont, rot_z)
    downHorizont2d = np.dot(downHorizont2d, rot_y)
    downHorizont2d = np.dot(downHorizont2d, rot_x)

    projected2d = np.dot(downHorizont2d, projection_matrix)
    projected2d = np.array(projected2d)
    for horizintPoint in projected2d:
        x = int(horizintPoint[0] * scale) + circle_pos[0]
        y = int(horizintPoint[1] * scale) + circle_pos[1]
        pygame.draw.circle(screen, (255,255,255), (x, y-135), 2)

    sleep(0.01)
    pygame.display.update()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pygame.quit()
            exit()
        if event.type == pg.KEYDOWN:
            #if event.key == pg.K_q:
            #    moving_matrix[0] = True
            #elif event.key == pg.K_e:
            #    moving_matrix[1] = True
            #elif event.key == pg.K_a:
            #    moving_matrix[2] = True
            #elif event.key == pg.K_d:
            #    moving_matrix[3] = True
            if event.key == pg.K_d:
                moving_matrix[4] = True
            elif event.key == pg.K_a:
                moving_matrix[5] = True
        if event.type == pg.KEYUP:
            
            if event.key == pg.K_d:
                moving_matrix[4] = False
            elif event.key == pg.K_a:
                moving_matrix[5] = False

    if moving_matrix[0]:
        angleZ += SPEED
    if moving_matrix[1]:
        angleZ -= SPEED
    if moving_matrix[4]:
        angleX += SPEED
    if moving_matrix[5]:
        angleX -= SPEED
    if moving_matrix[2]:
        angleY -= SPEED
    if moving_matrix[3]:
        angleY += SPEED
