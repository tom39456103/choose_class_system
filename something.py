from pygame import draw
from math import cos, sin, radians, pi

# 設置顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLACK = (10, 10, 10)
CLAY = (128,128,128)
DARKCLAY = (200,200,200)
RED = (255, 80, 80)
ORANGE = (239, 134, 0)
GREEN = (102, 153, 0)
BLUE = (51, 102, 204)

def piechart(screen, origin: tuple, radius, percentage: list):
    colors = [RED, ORANGE, GREEN, BLUE]  # 每個部分的顏色
    start_angle = -90
    length = len(percentage)
    vertex = []
    for i in range(length):
        vertex.append([])
    for j in range(length):
        for i in range(round(percentage[j] * 360.0 / 100)):
            vertex[j].append((origin[0] + radius * cos(radians(start_angle + i)),
                              origin[1] + radius * sin(radians(start_angle + i))))
            vertex[j].append(origin)
        draw.polygon(screen, colors[j], vertex[j], width=3)
        start_angle += round(percentage[j] * 360.0 / 100)
    draw.circle(screen, WHITE, origin, radius-6)

class grid():
    def __init__(self, rect: tuple[tuple, tuple], col, row) -> None:
        self.grid = self.gen_grid(rect, col, row)
        self.col = col
        self.row = row
        self.w = rect[1][0] / col
        self.h = rect[1][1] / row
        self.mid = (rect[1][0] / 2, rect[1][1] / 2)

    def gen_grid(self, rect: tuple[tuple, tuple], col, row):
        r = []
        for i in range(col):
            r.append([])
            for j in range(row):
                r[i].append((rect[0][0] + rect[1][0] * i / col,
                             rect[0][1] + rect[1][1] * j / row))
        return r
    
    def rect(self, rect: tuple[tuple, tuple]):
        return (self.grid[rect[0][0]][rect[0][1]],
                (rect[1][0] * self.w, rect[1][1] * self.h))
    
    def update(self, rect):
        self.grid = self.gen_grid(rect, self.col, self.row)
        self.w = rect[1][0] / self.col
        self.h = rect[1][1] / self.row
        self.mid = (rect[1][0] / 2, rect[1][1] / 2)