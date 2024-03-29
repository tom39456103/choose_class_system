from pygame import draw
import pygame
from math import cos, sin, radians, floor

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
        self.col = len(data[0])
        # p_grid的擷取
        self.grid = grid(p_grid.rect(rect), self.col, self.row) 
        # 表格顯示區的大小
        self.t_rect = ((rect[0][0], rect[0][1]+1), (rect[1][0], rect[1][1]-1))
        # 表格顯示區的畫布
        self.t_screen = pygame.Surface(p_grid.rect(self.t_rect)[1])
        self.t_grid = grid(((0, 0), (self.col * self.grid.w, (len(self.data) - 1) * self.grid.h)), 
                           self.col, (len(self.data) - 1))
        self.pos = 0        # 表格的位移
        self.volacity = 0   # 表格的移動速度
        self.font = pygame.font.Font("font.ttf", round(self.t_grid.w / 10))

    def draw(self, screen):
        '''畫表格'''
        # 表格的順暢滾動
        self.pos += self.volacity
        if self.volacity != 0:
            self.volacity *= 0.8
            floor(self.volacity)
            
        buttom = -self.grid.h * (len(self.data) - self.grid.row - 1)
        # 表格位移如果超出界線的話
        if self.pos < buttom:
            self.pos = buttom
        if self.pos > 0:
            self.pos = 0
        
        # 表格的底
        draw.rect(screen, self.colorset[0], 
                  self.p_grid.rect(self.rect), 
                  0, round(self.p_grid.h / 2))
        for i in range(self.col):
            # 顯示表格首列
            text = self.font.render(self.data[0][i], True, BLACK)
            text_rect = text.get_rect()
            text_rect.center = (self.grid.grid[i][0][0] + self.grid.w / 2, 
                                self.grid.grid[i][0][1] + self.grid.h / 2)
            screen.blit(text, text_rect)
        
        # 表格顯示區
        self.t_screen.fill(self.colorset[0])
        for i in range(1, len(self.data)-1):
        # 畫每列的分隔線，self.pos是位移
            draw.line(self.t_screen, self.colorset[3], 
                      (0, self.grid.h * i + self.pos), 
                      (self.grid.w * self.grid.col, self.grid.h * i + self.pos))
            for j in range(len(self.data[i])):
                # 畫文字
                if type(self.data[i][j]) == int or type(self.data[i][j]) == float :
                    d = str(self.data[i][j])
                else:
                    d = self.data[i][j]
                text = self.font.render(d, True, BLACK)
                text_rect = text.get_rect()
                text_rect.center = (self.t_grid.grid[j][i - 1][0] + self.t_grid.w / 2, 
                                    self.t_grid.grid[j][i - 1][1] + self.t_grid.h / 2 + self.pos)
                #print(d)
                self.t_screen.blit(text, text_rect)
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
        buttom = -self.grid.h * (len(self.data) - self.grid.row - 1)
        # 當滑鼠在表格內
        if self.in_table(m_pos):
            # 滑鼠往上滾
            if self.pos < 0 and event == 4:
                self.volacity += self.grid.h / 6
            # 滑鼠往下滾
            if self.pos > buttom and event == 5:
                self.volacity -= self.grid.h / 6
            

    def update(self):
        # 更新網格
        self.grid.update(self.p_grid.rect(self.rect))
        self.t_grid.update(((0, 0), (self.col * self.grid.w, (len(self.data) - 1) * self.grid.h)))
        # 更新表格顯示區的大小
        self.t_screen = pygame.Surface(self.p_grid.rect(self.t_rect)[1])
        # 更新字體
        self.font = pygame.font.Font("font.ttf", round(self.t_grid.w / 10))
        

