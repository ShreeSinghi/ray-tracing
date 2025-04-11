import pygame
import numpy as np

from player import Player
from map import Map

# class player():
    
#     def __init__(self, x, y, width, height):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.vel = 8
#         self.isjump = False
#         self.face = 'right'
#         self.jumpcount = 10
#         self.hitbox = (self.x,self.y,width,height)
        
#     def draw(self, win):
#         win.blit(walkleft if self.face == 'left' else walkright,(self.x, self.y))
#         self.hitbox=(self.x, self.y, self.width, self.height)
#         #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

#     def hit(self):
#         global score
        
#         fonthit = pygame.font.SysFont('comicsans', 100)
#         text = fonthit.render('You were hit!', 1, (255,0,0))
#         win.blit(text, (SCREEN_WIDTH/2-text.get_width()/2,SCREEN_HEIGHT/2))
#         score -= 5
#         pygame.display.update()

#         self.x = 20
#         self.y = 400
#         self.isjump = False
#         self.jumpcount = 10

#         i = 0
#         while i < 200:
#             pygame.time.delay(10)
#             i += 1
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     i = 301
#                     pygame.quit()


# class enemy():
#     walkright = pygame.image.load('source\\blueright.gif')
#     walkleft = pygame.transform.flip(walkright,True,False)

#     def __init__(self, x, y, width, height, end):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.end = end
#         self.path = (self.x, self.end)
#         self.vel = 4
#         self.hitbox = (self.x, self.y, self.width, self.height)
#         self.health = 10
#         self.visible = True

    
#     def draw(self,win):
#         if self.visible:
#             self.move()
#             win.blit(self.walkright if self.vel > 0 else self.walkleft, (self.x,self.y))
            
#             pygame.draw.rect(win, (255,0,0),(self.x + (self.width-50)/2, self.y-20, 50, 10))
#             pygame.draw.rect(win, (0,255,0),(self.x + (self.width-50)/2, self.y-20,(self.health*50/10), 10))
            
#             self.hitbox = (self.x,self.y,self.width,self.height)
#             #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        
    
#     def move(self):
#         if self.vel >= 0:
#             if self.x < self.path[1]:
#                 self.x += self.vel
#             else:
#                 self.vel *= -1
        
#         else:
#             if self.x-self.vel > self.path[0]:
#                 self.x += self.vel
#             else:
#                 self.vel *= -1

#     def hit(self):
#         if self.health > 1:
#             self.health -= 1
#         else:
#             self.visible = False
#         print('AAHH!!')
        
# def redraw():
#     win.blit(bg, (0,0))

#     text = font.render('Score: ' + str(score), 1, (255,255,255))
#     win.blit(text, (360, 10))
    
#     red.draw(win)
#     blue.draw(win)
#     for bullet in bullets:
#         bullet.draw(win)
    


pygame.init()


SCREEN_WIDTH  = 1000
SCREEN_HEIGHT = 500

RAY_COUNT = 1_000
HALF_FOV = np.arctan(np.pi * 2/3)  # this is width, assumed by default 
WALL_HEIGHT = 0.5

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
win.fill([255, 255, 255])

pygame.display.set_caption('Rate racer!')

# music = pygame.mixer.music.load('source\\bgmusic.mp3')
# pygame.mixer.music.play(-1)

clock = pygame.time.Clock()
font = pygame.font.SysFont('comicsans', 30, True)

player = Player((250, 250), 0)
map = Map("./map.png", player)
run = True

ray_angles = np.arctan(np.linspace(-1, 1, RAY_COUNT) * np.tan(HALF_FOV))
ray_xs  = np.linspace(-1, 1, RAY_COUNT) * SCREEN_WIDTH/2
ray_x_delta = ray_xs[1] - ray_xs[0]
depths  = np.zeros(RAY_COUNT)
colours = np.zeros((RAY_COUNT, 3))

while run:
    clock.tick(35)
    for i, ray_angle in enumerate(ray_angles):
        depths[i], colours[i] = map.emit_ray(ray_angle)
    
    for ray_x, depth, colour in zip(ray_xs, depths, colours):
        height = WALL_HEIGHT / depth * SCREEN_HEIGHT
        pygame.draw.rect(
            win,
            colour,
            (
                round(SCREEN_WIDTH/2 + ray_x - ray_x_delta/2),
                round(SCREEN_HEIGHT/2 - height/2),
                round(ray_x_delta),
                round(height)
            )
        )
    pygame.display.update()

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.rotate(-0.01)
        
    if keys[pygame.K_RIGHT]:
        player.rotate(0.01)
        
    if keys[pygame.K_UP]:
        player.move(0.1)

    if keys[pygame.K_DOWN]:
        player.move(-0.1)

pygame.quit()
