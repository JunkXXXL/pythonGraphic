import time
from math import tan, pi
from Camera import Camera
import numpy as np

import pygame as pg

from DrawObjects import DrawObject


pg.init()
W, H = 500, 500
screen = pg.display.set_mode((W, H))

camera = Camera(screen)
camera.look_at(1, 1, 1)
camera.ortho(W//2, H//2, 1)

running = True
Xmax, Xmin = 2, -2
Ymax, Ymin = 0, -2


def Bird(x, y) -> np.array:
    x = np.asarray(x)
    y = np.asarray(y)
    
    return np.absolute(x) * np.absolute(y)

figs = []
for i in range(10):
    for j in range(10):
        figs.append([i, j, Bird(i,j)])
figs = np.array(figs)

while running:
    screen.fill((0, 0, 0))

    camera.draw_figure(figs)
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    pg.display.update()
    time.sleep(0.05)

pg.quit()