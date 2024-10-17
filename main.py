import time
from math import tan, pi
from Camera import Camera

import pygame as pg
import numpy as np

from DrawObjects import DrawObject

pg.init()
W, H = 500, 500
screen = pg.display.set_mode((W, H))
pos = [[0, 0, 0], [0, 2, 0], [1, 0, 0], [1, 2, 0]]
alpha = 30
size = 10
angle = 90 - alpha
camera = Camera(screen)

obj = DrawObject(pos, [[0, 1], [0, 2], [1, 3], [2, 3]], [0,1,2])
obj.resize(size)
obj.displace([-W//2, H, 0])
obj.set_angle_z(angle)
obj.move_origins([-1, 0, 0])

vertexes = [[6, 0, 0], [3, 5.19, 0], [-3, 5.19, 0], [-6, 0, 0], [-3, -5.19, 0], [3, -5.19, 0],
            [6, 0, 20], [3, 5.19, 20], [-3, 5.19, 20], [-6, 0, 20], [-3, -5.19, 20], [3, -5.19, 20],
            [0, 0, 28]]

faced = [[0,1,2,3,4,5], [0,5,11,6,-1,-1], [1,0,6,7,-1,-1], [1,2,8,7,-1,-1], [3,4,10,9,-1,-1], [2,3,9,8, -1,-1],
         [4,5,11,10,-1,-1], [7,6,12, -1,-1,-1], [8,7,12, -1,-1,-1], [8,9,12, -1,-1,-1], [10,9,12, -1,-1,-1], [11,10,12, -1,-1,-1],
         [6,11,12, -1,-1,-1]]

lines = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 0],
                               [6, 7], [7, 8], [8, 9], [9, 10], [10, 11], [11, 6],
                               [6, 0], [7, 1], [8, 2], [9, 3], [10, 4], [11, 5],
                               [12, 6], [12, 7], [12, 8], [12, 9], [12, 10], [12, 11]]

pencil = DrawObject(vertexes, lines, faced)
pencil.resize(size)
pencil.displace([W//2, H, 0])
pencil.set_angle_y(30)

def Bird(x, y) -> np.array:
    x = np.asarray(x)
    y = np.asarray(y)
    
    return np.absolute(x) * np.absolute(y)

figs = []
for i in range(10):
    for j in range(10):
        figs.append([i*10 - 150, j*10 + 50, Bird(i,j)*10 - 260])
figs = np.array(figs)

origins_moving = [[0, -2, 0], [1, 0, 0], [0, 2, 0], [-1, 0, 0]]
origins_moving_counter = 0

camera.look_at(1, 1, 1)
camera.ortho(W//2, H//2, 1)

running = True
moving_matrix = [False, False, False, False, False, False]
SPEED = 0.1

while running:
    screen.fill((0, 0, 0))

    #camera.draw(obj)
    camera.draw(pencil)
    #camera.draw_center()
    #camera.draw_figure(figs)
    pg.display.update()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                moving_matrix[0] = True
            elif event.key == pg.K_e:
                moving_matrix[1] = True
            elif event.key == pg.K_a:
                moving_matrix[2] = True
            elif event.key == pg.K_d:
                moving_matrix[3] = True
            elif event.key == pg.K_w:
                moving_matrix[4] = True
            elif event.key == pg.K_s:
                moving_matrix[5] = True
            elif event.key == pg.K_LSHIFT:
                camera.ortho(W//2, H//2, 2)
            elif event.key == pg.K_LCTRL:
                camera.ortho(W//2, H//2, 1)
            print(f"coordinates: {camera.x, camera.y, camera.z}")
        if event.type == pg.KEYUP:
            if event.key == pg.K_q:
                moving_matrix[0] = False
            elif event.key == pg.K_e:
                moving_matrix[1] = False
            elif event.key == pg.K_a:
                moving_matrix[2] = False
            elif event.key == pg.K_d:
                moving_matrix[3] = False
            elif event.key == pg.K_w:
                moving_matrix[4] = False
            elif event.key == pg.K_s:
                moving_matrix[5] = False

    if moving_matrix[0]:
        camera.look_at(camera.x, camera.y, camera.z + SPEED)
    if moving_matrix[1]:
        camera.look_at(camera.x, camera.y, camera.z - SPEED)
    if moving_matrix[2]:
        camera.look_at(camera.x + SPEED, camera.y, camera.z)
    if moving_matrix[3]:
        camera.look_at(camera.x - SPEED, camera.y, camera.z)
    if moving_matrix[4]:
        camera.look_at(camera.x, camera.y - SPEED, camera.z)
    if moving_matrix[5]:
        camera.look_at(camera.x, camera.y + SPEED, camera.z)

    angle -= 2
    obj.set_angle_z(angle)
    pencil.set_angle_z(angle)
    if (angle + alpha) % 90 == 0:
        obj.move_origins(origins_moving[origins_moving_counter])
        obj.move([-origins_moving[origins_moving_counter][0]*size,
                  -origins_moving[origins_moving_counter][1]*size,
                  0])
        origins_moving_counter = (origins_moving_counter + 1) % 4

    time.sleep(0.05)


pg.quit()
