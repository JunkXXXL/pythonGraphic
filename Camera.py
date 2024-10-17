import numpy as np
from DrawObjects import DrawObject
from pygame import Surface, draw, font


def _get_face_array_len(array: np.array) -> int:
    len_array = len(array)
    for i in np.arange(len_array):
        if array[i] == -1:
            return i
    return len_array


class Camera:
    def __init__(self, screen: Surface):
        self.x = 0
        self.y = 0
        self.z = 0

        self.__screen = screen
        self.__matrixView = 0
        self.__matrixProjection = 0

        self.font = font.SysFont(None, 24)

    def look_at(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

        matrix_t = np.asarray([[1, 0, 0, 0],
                             [0, 1, 0, 0],
                             [0, 0, 1, 0],
                             [-self.x, -self.y, -self.z, 1]], dtype='float')

        matrix_s = np.asarray([[-1, 0, 0, 0],
                             [0,  1, 0, 0],
                             [0,  0, 1, 0],
                             [0, 0, 0, 0]], dtype='float')

        matrix_r90 = np.asarray([[1, 0, 0, 0],
                               [0, 0, -1, 0],
                               [0, 1, 0, 0],
                               [0, 0, 0, 1]], dtype='float')

        d = np.sqrt(self.x**2 + self.y**2)
        c = s = 0
        if d == 0:
            c = 1
            s = 1
        else:
            c = self.y/d
            s = self.x/d

        matrix_ru = np.asarray([[c, 0, s, 0],
                              [0, 1, 0, 0],
                              [-s, 0, c, 0],
                              [0, 0, 0, 1]], dtype='float')

        l = np.sqrt(d * d + self.z * self.z)

        if l == 0:
            c = 1
            s = 0
        else:
            c = d / l
            s = self.z / l

        matrix_rw = np.asarray([[1, 0, 0, 0],
                              [0, c, -s, 0],
                              [0, s, c, 0],
                              [0, 0, 0, 1]], dtype='float')

        self.__matrixView = np.dot(np.dot(np.dot(np.dot(matrix_t, matrix_s), matrix_r90), matrix_ru), matrix_rw)

    def ortho(self, offset_x, offset_y, zoom):
        self.__matrixProjection = np.array([[zoom, 0, 0, 0],
                                            [0, -zoom, 0, 0],
                                            [0, 0, 0, 0],
                                            [offset_x, offset_y, 0, 1]])

    def draw(self, figure: DrawObject):
        points_3d = figure.get_draw_points()
        
        points_3d = np.hstack([points_3d, np.ones((points_3d.shape[0], 1))])

        points = np.dot(np.dot(points_3d, self.__matrixView), self.__matrixProjection)

        #Center of object
        center_point_3d = figure.get_center_points()
        center_point_3d = np.hstack([center_point_3d, np.array([1])])
        center_point = np.dot(np.dot(center_point_3d, self.__matrixView), self.__matrixProjection)
        draw.circle(self.__screen, (255,0,0), center_point[:2], 5, 5)

        #decision which face is draw
        for face in figure.faces:
            A, B, C, D = figure.find_flat_coef(points_3d[face[0]], points_3d[face[1]], points_3d[face[2]])
            if figure.is_faced(A, B, C, D, self.x, self.y, self.z, center_point_3d[0], center_point_3d[1], center_point_3d[2]):
                face_array_len = _get_face_array_len(face)

                img1 = self.font.render(str(face[0]), True, (0, 0, 255))
                self.__screen.blit(img1, points[face[0]][:2])
                
                for i in np.arange(face_array_len):
                    draw.line(self.__screen, figure.color, points[face[i]][:2], points[face[(i+1)%face_array_len]][:2])

    def draw_center(self):
        x, y = self.__screen.get_size()
        points = [x//2, y//2, 0, 1]
        points = np.dot(np.dot(points, self.__matrixView), self.__matrixProjection)
        draw.circle(self.__screen, (255, 0, 0), points[:2], 5)

    def draw_figure(self, cords: np.array):
        cords = np.hstack([cords, np.ones([cords.shape[0], 1])])
        #print()
        #print(cords[0], cords[55])
        cords = np.dot(cords, self.__matrixView)
        #print(cords[0], cords[55])
        cords = np.dot(cords, self.__matrixProjection)
        #print(cords[0], cords[55])
        for cord in cords:
            draw.circle(self.__screen, (255, 0, 0), cord[:2], 5)
