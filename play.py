import pygame
import math

# 從文件中讀取課程數據列表
def load_course_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        courses = [line.strip() for line in file]
    return courses

# 從文件中加載課程數據列表
course_data = load_course_data('courses.txt')

# 初始化 Pygame
pygame.init()

# 設置視窗大小和標題
WINDOW_SIZE = (800, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("課程信息")

# 設置顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# 加載字體
font = pygame.font.SysFont("font.ttf", 24)
# 數據 - 用於繪製圓餅圖
data = [30, 20, 25, 25]  # 例如，這裡表示四個部分，佔比分別為 30%，20%，25%，25%
total = sum(data)
start_angle = 0
angles = [360 * value / total for value in data]

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
    running = True
while running:
    screen.fill(WHITE)

    # #1 在畫面中上圓餅圖呈現
    radius = 100
    center = (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 4)
    colors = [RED, GREEN, BLUE, BLACK]  # 每個部分的顏色

    for i, angle in enumerate(angles):
        pygame.draw.polygon(screen, colors[i], [center, (center[0] + radius * math.cos(math.radians(start_angle)),
                                                     center[1] + radius * math.sin(math.radians(start_angle))),
                                                (center[0] + radius * math.cos(math.radians(start_angle + angle)),
                                                 center[1] + radius * math.sin(math.radians(start_angle + angle)))])
        start_angle += angle

    # #2 在右上角長方形呈現
    rect1 = pygame.Rect(600, 50, 100, 200)
    pygame.draw.rect(screen, RED, rect1)

    # #3 在右下角長方形呈現
    rect2 = pygame.Rect(600, 400, 150, 50)
    pygame.draw.rect(screen, BLUE, rect2)

    # #4 在左邊長方形呈現
    rect3 = pygame.Rect(50, 200, 200, 100)
    pygame.draw.rect(screen, GREEN, rect3)

    # 更新顯示
    pygame.display.flip()
    # 處理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

# 退出 Pygame
pygame.quit()
