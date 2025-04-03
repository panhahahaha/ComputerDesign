import pygame

# 初始化 Pygame
pygame.init()

# 设置屏幕尺寸
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("笑脸表情")

# 设置颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# 创建屏幕
screen.fill(BLACK)

# 绘制笑脸
center = (200, 200)  # 笑脸中心位置
radius = 100  # 笑脸半径
eye_radius = 10  # 眼睛半径

# 画出笑脸轮廓
pygame.draw.circle(screen, YELLOW, center, radius, 2)

# 画出眼睛
pygame.draw.circle(screen, WHITE, (160, 170), eye_radius)  # 左眼
pygame.draw.circle(screen, WHITE, (240, 170), eye_radius)  # 右眼

# 画出笑嘴
# pygame.draw.arc(screen, WHITE, (130, 220, 140, 60), 3.14, 0, 2)
pygame.draw.arc(screen, WHITE, (130, 220, 140, 60), 0, 3.14, 2)

# 刷新屏幕显示
pygame.display.flip()

# 等待用户关闭窗口
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# 退出Pygame
pygame.quit()
