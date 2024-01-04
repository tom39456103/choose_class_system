from pygame import draw
import pygame
from math import cos, sin, radians, pi

# 設置顏色
WHITE = (255, 255, 255)
BLACK = (10, 10, 10)
CLAY = (128,128,128)
DARKCLAY = (200,200,200)
# 中，深，淺，更淺
GRAY = [(174, 188, 196), (142, 161, 172), (198, 208, 214), (228, 233, 235)]
RED = [(255, 80, 80), (204, 0, 0), (255, 124, 128), (255, 204, 204)]
ORANGE = [(239, 134, 0), (204, 102, 0), (255, 171, 64), (255, 205,140)]
GREEN = [(102, 153, 0), (51, 102, 0), (153, 204, 0), (245, 255, 141)]
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
        # 網格到像素
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
        self.p_grid = p_grid    # 背景的網格
        self.rect = rect        # 背景網格單位下的rect座標
        self.row = rect[1][1]   # 背景網格單位下，這個table的高度
        self.grid = grid(p_grid.rect(rect), len(data[0]), self.row) # p_grid的擷取
        self.t_rect = ((rect[0][0], rect[0][1]+1), (rect[1][0], rect[1][1]-1))
        self.t_screen = pygame.Surface(p_grid.rect(self.t_rect)[1])
        self.pos = 0

    def draw(self, screen):
        draw.rect(screen, self.colorset[0], 
                  self.p_grid.rect(self.rect), 
                  0, round(self.p_grid.h / 2))
        self.t_screen.fill(self.colorset[0])
        for i in range(0, len(self.data)-1):
            draw.line(self.t_screen, self.colorset[3], 
                      (0, self.grid.h * i + self.pos), 
                      (self.grid.w * self.grid.col, self.grid.h * i + self.pos))
        draw.line(self.t_screen, self.colorset[1], 
                  (0, 0), (self.grid.w * self.grid.col, 0), 2)
            
        screen.blit(self.t_screen, self.grid.grid[0][1])

    def in_table(self, m: tuple):
        '''判斷滑鼠位置是否在表格中'''
        x1 = self.grid.grid[0][1][0]
        x2 = x1 + self.grid.w * self.grid.col
        y1 = self.grid.grid[0][1][1]
        y2 = y1 + self.grid.h * self.grid.row
        return (x1 <= m[0] <= x2) and (y1 <= m[1] <= y2)

    def mouse_scroll(self, m_pos, event):
        if self.in_table(m_pos) and self.pos < 0 and event == 4:
            self.pos += self.grid.h / 4
            if self.pos < -self.grid.h * (len(self.data) - self.grid.row):
                self.pos = self.grid.h * (len(self.data) - self.grid.row)
        if self.in_table(m_pos) and self.pos > -self.grid.h * (len(self.data) - self.grid.row) and event == 5:
            self.pos -= self.grid.h / 4
            if self.pos > 0:
                self.pos = 0

    def update(self):
        self.grid.update(self.p_grid.rect(self.rect))
        self.t_screen = pygame.Surface(self.p_grid.rect(self.t_rect)[1])
        

