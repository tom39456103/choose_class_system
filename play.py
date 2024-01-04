import pygame
from pygame import draw
from something import *

# # 從文件中讀取課程數據列表
# def load_course_data(filename):
#     with open(filename, 'r', encoding='utf-8') as file:
#         courses = [line.strip() for line in file]
#     return courses

# # 從文件中加載課程數據列表
# course_data = load_course_data('courses.txt')
course_data = ['1', '2', '3', '4']

# 初始化 Pygame
pygame.init()

# 設置視窗大小和標題
WINDOW_SIZE = (800, 600)
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
pygame.display.set_caption("課程信息")
grid1 = grid(((0, 0), WINDOW_SIZE), 20, 12)

# 加載字體
font = pygame.font.SysFont("font.ttf", 24)
# 數據 - 用於繪製圓餅圖
data = [30, 20, 25, 25]  # 例如，這裡表示四個部分，佔比分別為 30%，20%，25%，25%

t_data = [[1, 2, 3, 4], 2, 3, 4, 5, 6]
table2 = table(t_data, GRAY, grid1, ((13, 1), (6, 4)))
table3 = table(t_data, GRAY, grid1, ((8, 6), (11, 5)))
table4 = table(t_data, GRAY, grid1, ((1, 1), (6, 10)))

# 主循環
running = True
while running:
    screen.fill(WHITE)

    # 顯示課程信息
    y = 50
    for course in course_data:
        course_text = font.render(course, True, BLACK)
        screen.blit(course_text, (50, y))
        y += 40

    # #1 在畫面中上圓餅圖呈現
    radius = min(grid1.h, grid1.w) * 2
    center = grid1.grid[10][3]
    piechart(screen, center, radius, data)

    # #2 在右上角長方形呈現
    table2.draw(screen)

    # #3 在右下角長方形呈現
    table3.draw(screen)

    # #4 在左邊長方形呈現
    table4.draw(screen)

    # 更新顯示
    pygame.display.flip()
    # 處理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            WINDOW_SIZE = (event.w,event.h)
            window = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
            grid1.update(((0, 0), WINDOW_SIZE))
            table2.update()
            table3.update()
            table4.update()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            table2.mouse_scroll(pygame.mouse.get_pos(), event.button)
            table3.mouse_scroll(pygame.mouse.get_pos(), event.button)
            table4.mouse_scroll(pygame.mouse.get_pos(), event.button)

    pygame.display.flip()

# 退出 Pygame
pygame.quit()

