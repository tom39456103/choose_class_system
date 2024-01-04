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
    '''畫圓餅圖'''
    colors = [RED[0], ORANGE[0], GREEN[0], BLUE[0]]  # 每個部分的顏色
    start_angle = -90   # 正上方，角度制
    length = len(percentage)    # 資料的長度
    vertex = []

    # 為每個資料設一個扇形的邊
    for i in range(length):
        vertex.append([])
    for j in range(length):
        for i in range(round(percentage[j] * 360.0 / 100)):
            # 在每一度加入圓周
            vertex[j].append((origin[0] + radius * cos(radians(start_angle + i)),
                              origin[1] + radius * sin(radians(start_angle + i))))
            # 加入原點
            vertex[j].append(origin)
        # 畫出扇形
        draw.polygon(screen, colors[j], vertex[j], width=8)
        # 重設起始角
        start_angle += round(percentage[j] * 360.0 / 100)
    # 最後，在中心用一個小圓覆蓋
    draw.circle(screen, WHITE, origin, radius-6)

class grid():
    def __init__(self, rect: tuple[tuple, tuple], col, row):
        self.grid = self.gen_grid(rect, col, row)
        self.col = col  # 網格的列數
        self.row = row  # 網格的行數
        self.w = rect[1][0] / col   # 每一小格的寬度
        self.h = rect[1][1] / row   # 每一小格的高度
        self.mid = (rect[1][0] / 2, rect[1][1] / 2) # 網格中心

    def gen_grid(self, rect: tuple[tuple, tuple], col, row):
        '''生成網格'''
        r = []
        for i in range(col+1):
            r.append([])
            for j in range(row+1):
                # 把螢幕位置塞入網格的每個節點
                r[i].append((rect[0][0] + rect[1][0] * i / col,
                             rect[0][1] + rect[1][1] * j / row))
        return r
    
    def rect(self, rect: tuple[tuple, tuple]):
        '''網格到像素'''
        return (self.grid[rect[0][0]][rect[0][1]], (rect[1][0] * self.w, rect[1][1] * self.h))
    
    def update(self, rect):
        '''當螢幕大小改變，則網格需要更新'''
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
        # p_grid的擷取
        self.grid = grid(p_grid.rect(rect), len(data[0]), self.row) 
        # 表格顯示區的大小
        self.t_rect = ((rect[0][0], rect[0][1]+1), (rect[1][0], rect[1][1]-1))
        # 表格顯示區的畫布
        self.t_screen = pygame.Surface(p_grid.rect(self.t_rect)[1])
        self.pos = 0

    def draw(self, screen):
        '''畫表格'''
        # 表格的底
        draw.rect(screen, self.colorset[0], 
                  self.p_grid.rect(self.rect), 
                  0, round(self.p_grid.h / 2))
        
        # 表格顯示區
        self.t_screen.fill(self.colorset[0])
        # 畫每列的分隔線，self.pos是位移
        for i in range(0, len(self.data)-1):
            draw.line(self.t_screen, self.colorset[3], 
                      (0, self.grid.h * i + self.pos), 
                      (self.grid.w * self.grid.col, self.grid.h * i + self.pos))
        # 畫首列的分隔線
        draw.line(self.t_screen, self.colorset[1], 
                  (0, 0), (self.grid.w * self.grid.col, 0), 2)
        
        # 融合兩個畫布
        screen.blit(self.t_screen, self.grid.grid[0][1])

    def in_table(self, m: tuple):
        '''判斷滑鼠位置是否在表格中'''
        x1 = self.grid.grid[0][1][0]
        x2 = x1 + self.grid.w * self.grid.col
        y1 = self.grid.grid[0][1][1]
        y2 = y1 + self.grid.h * self.grid.row
        return (x1 <= m[0] <= x2) and (y1 <= m[1] <= y2)

    def mouse_scroll(self, m_pos, event):
        '''滑鼠滾動的行為'''
        # 當滑鼠在表格內
        if self.in_table(m_pos):
            # 滑鼠往上滾
            # 表格在頂部時，不能往下滑
            if self.pos < 0 and event == 4:
                self.pos += self.grid.h / 4
                # 超出的話
                if self.pos < -self.grid.h * (len(self.data) - self.grid.row):
                    self.pos = self.grid.h * (len(self.data) - self.grid.row)
            
            # 滑鼠往下滾
            # 表格在底部時，不能往上滑
            if self.pos > -self.grid.h * (len(self.data) - self.grid.row) and event == 5:
                self.pos -= self.grid.h / 4
                # 超出的話
                if self.pos > 0:
                    self.pos = 0

    def update(self):
        # 更新網格
        self.grid.update(self.p_grid.rect(self.rect))
        # 更新表格顯示區的大小
        self.t_screen = pygame.Surface(self.p_grid.rect(self.t_rect)[1])
        

