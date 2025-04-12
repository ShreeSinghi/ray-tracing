import pygame
import numpy as np

from player import Player
from map import Map

pygame.init()


SCREEN_WIDTH  = 1_500
SCREEN_HEIGHT = 800

RAY_COUNT = 50
HALF_FOV = np.arctan(np.pi * 1/4)  # this is width, assumed by default 
WALL_HEIGHT = 20

ROTATING_SPEED = 0.1
MOVEMENT_SPEED = 5

SKY_BLUE = [90, 120, 255]
GREEN = [150, 200, 150]
WHITE = [255, 255, 255]

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
win.fill(WHITE)

pygame.display.set_caption('Rate racer!')

# music = pygame.mixer.music.load('source\\bgmusic.mp3')
# pygame.mixer.music.play(-1)

clock = pygame.time.Clock()
font = pygame.font.SysFont('comicsans', 30, True)

player = Player((250, 250), np.pi/2)
map = Map("./map.png", player)

run = True

ray_angles = np.arctan(np.linspace(-1, 1, RAY_COUNT) * np.tan(HALF_FOV))
ray_xs  = np.linspace(-1, 1, RAY_COUNT) * SCREEN_WIDTH/2
ray_x_delta = ray_xs[1] - ray_xs[0]

while run:
    clock.tick(200)
    depths, colours = map.emit_rays(ray_angles)

    win.fill(SKY_BLUE)
    pygame.draw.rect(win, GREEN, (0, SCREEN_HEIGHT//2, SCREEN_WIDTH, SCREEN_HEIGHT//2))
    for ray_x, depth, colour in zip(ray_xs, depths, colours):
        height = min(WALL_HEIGHT / depth * SCREEN_HEIGHT, SCREEN_HEIGHT)   # clip so fatte na
        vertical_displacement = min(player.z / depth * SCREEN_HEIGHT, SCREEN_HEIGHT)

        pygame.draw.rect(
            win,
            colour,
            (
                np.floor(SCREEN_WIDTH/2 + ray_x - ray_x_delta/2),
                round(SCREEN_HEIGHT/2 - height/2 + vertical_displacement),
                np.ceil(ray_x_delta),
                round(height)
            )
        )
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.rotate(-ROTATING_SPEED)
        
    if keys[pygame.K_RIGHT]:
        player.rotate(ROTATING_SPEED)
        
    if keys[pygame.K_UP]:
        player.move(MOVEMENT_SPEED)

    if keys[pygame.K_DOWN]:
        player.move(-MOVEMENT_SPEED)

    if keys[pygame.K_SPACE]:
        player.jump() 
    player.gravity_update()

pygame.quit()
