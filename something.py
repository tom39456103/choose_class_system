from pygame import draw
from math import cos, sin, radians, pi

# 設置顏色
WHITE = (255, 255, 255)
BLACK = (10, 10, 10)
CLAY = (128,128,128)
DARKCLAY = (200,200,200)
# 中，深，淺，更淺
RED = [(255, 80, 80), (204, 0, 0), (255, 124, 128), (255, 204, 204)]
ORANGE = [(239, 134, 0), (204, 102, 0), (255, 171, 64), (255, 205,140)]
GREEN = [(102, 153, 0), (51, 102, 0), (153, 204, 0), (219, 240, 0)]
BLUE = [(51, 102, 204), (9, 60, 146), (66, 133, 244), (142, 182, 248)]

def piechart(screen, origin: tuple, radius, percentage: list):
    colors = [RED[0], ORANGE[0], GREEN[0], BLUE[0]]  # 每個部分的顏色
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
        draw.polygon(screen, colors[j], vertex[j], width=8)
        start_angle += round(percentage[j] * 360.0 / 100)
    draw.circle(screen, WHITE, origin, radius-6)

class grid():
    def __init__(self, rect: tuple[tuple, tuple], col, row):
        self.grid = self.gen_grid(rect, col, row)
        self.col = col
        self.row = row
        self.w = rect[1][0] / col
        self.h = rect[1][1] / row
        self.mid = (rect[1][0] / 2, rect[1][1] / 2)

    def gen_grid(self, rect: tuple[tuple, tuple], col, row):
        r = []
        for i in range(col+1):
            r.append([])
            for j in range(row+1):
                r[i].append((rect[0][0] + rect[1][0] * i / col,
                             rect[0][1] + rect[1][1] * j / row))
        return r
    
    def rect(self, rect: tuple[tuple, tuple]):
        return (self.grid[rect[0][0]][rect[0][1]], (rect[1][0] * self.w, rect[1][1] * self.h))
    
    def update(self, rect):
        self.grid = self.gen_grid(rect, self.col, self.row)
        self.w = rect[1][0] / self.col
        self.h = rect[1][1] / self.row
        self.mid = (rect[1][0] / 2, rect[1][1] / 2)

class table():
    def __init__(self, data: list, colorset, p_grid: grid, rect):
        self.data = data
        self.colorset = colorset
        self.p_grid = p_grid
        self.rect = rect
        self.row = rect[1][1]
        self.grid = grid(p_grid.rect(rect), len(data[0]), self.row)

    def draw(self, screen):
        draw.rect(screen, self.colorset[2], 
                  self.p_grid.rect(self.rect), 
                  0, round(self.p_grid.h / 2))
        draw.line(screen, self.colorset[1], 
                  self.grid.grid[0][1], 
                  self.grid.grid[self.grid.col][1])
        for i in range(2, self.row):
            draw.line(screen, self.colorset[3], 
                      self.grid.grid[0][i], 
                      self.grid.grid[self.grid.col][i])
    
    def update(self):
        self.grid.update(self.p_grid.rect(self.rect))
        

