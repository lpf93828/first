#!/usr/bin/env python
#-*- coding:utf-8 -*-


import pygame, sys, random

# 滑雪人的不同状态图片文件
skier_images = ["skier_down.png", "skier_right1.png", "skier_right2.png",
                 "skier_left2.png", "skier_left1.png"]

# 滑雪人的类
class SkierClass(pygame.sprite.Sprite):
    def __init__(self):
    
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("skier_down.png") # 加载图片文件
        self.rect = self.image.get_rect()
        self.rect.center = [320, 100]            # 滑雪人的中心
        self.angle = 0                           # 滑雪角度
        
    def turn(self, direction): 
        # 转向函数返回转向后的速度
        self.angle = self.angle + direction
        
        # 只有四种角度
        if self.angle < -2:  
            self.angle = -2
        if self.angle >  2:  
            self.angle =  2
        
        center = self.rect.center
        # 加载对应速度的图片文件
        self.image = pygame.image.load(skier_images[self.angle])
        
        self.rect = self.image.get_rect()
        self.rect.center = center
        speed = [self.angle, 6 - abs(self.angle) * 2]
        return speed
    
    def move(self, speed):
    
        self.rect.centerx = self.rect.centerx + speed[0]
        
        # 不能过边界
        if self.rect.centerx < 20:  
            self.rect.centerx = 20
        if self.rect.centerx > 620: 
            self.rect.centerx = 620 
        
# 障碍物的类
class ObstacleClass(pygame.sprite.Sprite):

    def __init__(self, image_file, location, type):
        pygame.sprite.Sprite.__init__(self)
        
        self.image_file = image_file        
        self.image = pygame.image.load(image_file)
        
        self.location = location
        self.rect = self.image.get_rect()
        self.rect.center = location
        
        # 是树还是旗子
        self.type = type
        # 是否经过
        self.passed = False
    
    # 滚动场景
    def scroll(self, terrainPos):
        self.rect.centery = self.location[1] - terrainPos

# 生产场景,每个障碍物有64见方的大小,避免太近

def create_map(start, end):
    obstacles = pygame.sprite.Group()
    
    locations = []
    gates = pygame.sprite.Group()
    
    for i in range(10):                 # 每个场景10个障碍物
     
        row = random.randint(start, end)
        col = random.randint(0, 9)
        location  = [col * 64 + 20, row * 64 + 20] 
        # 避免重复的位置
        if not (location in locations):
            locations.append(location)
            
            # 加载不同的物品          
            type = random.choice(["tree", "flag"])
            if type == "tree": 
                img = "skier_tree.png"
            elif type == "flag":
                img = "skier_flag.png"
            
            # 产生物品
            obstacle = ObstacleClass(img, location, type)
            obstacles.add(obstacle)
    return obstacles

# 重绘场景
def animate():
    # 白色背景
    screen.fill([255, 255, 255])
    pygame.display.update(obstacles.draw(screen)) 
    screen.blit(skier.image, skier.rect)
    screen.blit(score_text, [10, 10])
    pygame.display.flip()    

# 更新障碍物
def updateObstacleGroup(map0, map1):

    obstacles = pygame.sprite.Group()
    
    for ob in map0:
        obstacles.add(ob)
        
    for ob in map1:
        obstacles.add(ob)
        
    return obstacles

# 初始化
pygame.init()
screen = pygame.display.set_mode([640,640])  # 窗口是640*640大小的
clock = pygame.time.Clock()

skier = SkierClass()
speed = [0, 6]

map_position = 0
points = 0                                   # 得分

map0 = create_map(20, 29)
map1 = create_map(10, 19)
activeMap = 0

# 所有的物品
obstacles = updateObstacleGroup(map0, map1)

# 字体
font = pygame.font.Font(None, 50)

# 循环主事件
while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
        if event.type == pygame.KEYDOWN:          # 是否按下键盘
            if event.key == pygame.K_LEFT:        # 按下左键
                speed = skier.turn(-1)
            elif event.key == pygame.K_RIGHT:     # 按下右键
                speed = skier.turn(1)

    skier.move(speed)                             # 滑雪人移动
    map_position += speed[1]                      # 场景移动
    
    # 绘制新的场景 activeMap表示是否要产生新的地图
    if map_position >= 640 and activeMap == 0:
        activeMap = 1
        map0 = create_map(20, 29)
        obstacles = updateObstacleGroup(map0, map1)
    
    if map_position >= 1280 and activeMap == 1:                        
        activeMap = 0
        for ob in map0:
            ob.location[1] -= 1280   
        map_position -= 1280
               
        map1 = create_map(10, 19)
        obstacles = updateObstacleGroup(map0, map1)
    
    # 滚动物品
    for obstacle in obstacles:
        obstacle.scroll(map_position)
    
    # 检测是否发生碰撞
    hit =  pygame.sprite.spritecollide(skier, obstacles, False)
    if hit:
        # 撞到树时候发生的事情
        if hit[0].type == "tree" and not hit[0].passed:   
            points -= 100
            skier.image = pygame.image.load("skier_crash.png")  
            
            animate()  
            pygame.time.delay(1000)
            
            skier.image = pygame.image.load("skier_down.png")  
            skier.angle = 0
            speed = [0, 6]
            hit[0].passed = True
        # 碰到旗子时候
        elif hit[0].type == "flag" and not hit[0].passed:   
            points += 10
            obstacles.remove(hit[0])                    
    
    score_text = font.render("Score: " + str(points), 1, (0, 0, 0))
    animate()
