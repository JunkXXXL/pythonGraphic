import pygame as pg
import numpy as np

from math import pi, sin, cos


class DrawObject:
    def __init__(self, cords: list, lines: list, faces: list):
        self.cords = np.array(cords)
        self.lines = np.array(lines)
        self.faces = np.array(faces)
        self.center_weigth()
        self.angle_z = 0
        self.angle_x = 0
        self.angle_y = 0
        self.size = 1
        self.transpose = np.array([0, 0, 0])
        self.angle = 0
        self.color = (255, 255, 255)

    def find_flat_coef(self, point1, point2, point3) -> list:
        A = (point3[1] - point1[1])*(point2[2] - point1[2]) - (point2[1] - point1[1])*(point3[2] - point1[2])
        B = (point2[0] - point1[0])*(point3[2] - point1[2]) - (point3[0] - point1[0])*(point2[2] - point1[2])
        C = (point3[0] - point1[0])*(point2[1] - point1[1]) - (point2[0] - point1[0])*(point3[1] - point1[1])
        
        D = -(A*point1[0] + B*point1[1] + C*point1[2])
        return [A, B, C, D]
    
    def is_faced(self, A, B, C, D, x, y, z, Xc, Yc, Zc) -> bool:
        if A*Xc + B*Yc + C*Zc + D < 0:
            A, B, C, D = -A, -B, -C, -D
        
        #print(A, B, C, D, A*x+B*y+C*z+D)
        if A*x+B*y+C*z < 0:
            return True
        return False

    def center_weigth(self) -> None:
        Nver = self.cords.shape[0]
        self.Xc = self.cords[:, 0].sum() / Nver
        self.Yc = self.cords[:, 1].sum() / Nver
        self.Zc = self.cords[:, 2].sum() / Nver

    def _draw_UI(self, screen: pg.Surface) -> None:
        draw_array = np.array(self.cords)
        draw_array = self._rotate_z(draw_array)
        draw_array = self._rotate_x(draw_array)
        draw_array = self._resize(draw_array)
        draw_array = self._displace(draw_array)
        for point in self.lines:
            pg.draw.line(screen, (255, 255, 255), draw_array[point[0]], draw_array[point[1]])

    def get_draw_points(self) -> np.ndarray:
        draw_array = np.array(self.cords)
        draw_array = self._rotate_z(draw_array)
        draw_array = self._rotate_x(draw_array)
        draw_array = self._rotate_y(draw_array)
        draw_array = self._resize(draw_array)
        draw_array = self._displace(draw_array)

        return draw_array
    
    def get_center_points(self) -> np.ndarray:
        center_points = np.array([self.Xc, self.Yc, self.Zc])
        center_points = self._rotate_z(center_points)
        center_points = self._rotate_x(center_points)
        center_points = self._rotate_y(center_points)
        center_points = self._resize(center_points)
        center_points = self._displace(center_points)

        return center_points

    def resize(self, size: float):
        self.size = size

    def displace(self, transpose: list):
        self.transpose = transpose

    def move(self, transpose: list):
        transpose = self._rotate_z(transpose)
        self.transpose = self.transpose + np.array(transpose)

    def set_angle_z(self, angle):
        self.angle_z = angle

    def set_angle_x(self, angle):
        self.angle_x = angle

    def set_angle_y(self, angle):
        self.angle_y = angle

    def move_origins(self, pos: list):
        self.cords = self.cords + pos

    def _resize(self, draw_array: np.array) -> np.array:
        return draw_array * self.size

    def _displace(self, draw_array: np.array) -> np.array:
        return draw_array + self.transpose

    def _rotate_z(self, draw_array: np.array) -> np.array:
        angle = self.angle_z / 180 * pi
        rotate_matrix = np.array([[sin(angle),  cos(angle), 0],
                                  [cos(angle), -sin(angle), 0],
                                  [0,           0,          1]])
        return np.dot(draw_array, rotate_matrix)

    def _rotate_x(self, draw_array: np.array) -> np.array:
        angle = self.angle_x / 180 * pi
        rotate_matrix = np.array([[1, 0, 0],
                                  [0, sin(angle), cos(angle)],
                                  [0, cos(angle), -sin(angle)]])
        return np.dot(draw_array, rotate_matrix)

    def _rotate_y(self, draw_array: np.array) -> np.array:
        angle = self.angle_y / 180 * pi
        rotate_matrix = np.array([[sin(angle), 0, cos(angle)],
                                  [0, 1, 0],
                                  [cos(angle), 0, -sin(angle)]])
        return np.dot(draw_array, rotate_matrix)
