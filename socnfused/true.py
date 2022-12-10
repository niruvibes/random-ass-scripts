import pygame
from pygame.locals import *
import sys

# initialize pygame
pygame.init()

# create the game window
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Platformer")

# create the game clock
clock = pygame.time.Clock()

# create the player character
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.jumping = False
        self.jump_speed = 10
        self.jump_time = 0

# create the platforms
class Platform:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

# create a player object at position (100, 100)
player = Player(100, 100)

# create some platforms
platforms = [
    Platform(100, 400, 100, 20),
    Platform(300, 300, 100, 20),
    Platform(500, 500, 100, 20),
]

# game loop
while True:
    try:
        # handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # update game state
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            player.x -= player.speed
        if keys[K_RIGHT]:
            player.x += player.speed

        # handle jumping
        if keys[K_SPACE] and not player.jumping:
            player.jumping = True
            player.jump_time = 10
        if player.jumping:
            player.y -= player.jump_time
            player.jump_time -= 1
            if player.jump_time == 0:
                player.jumping = False
        else:
            # apply gravity
            player.y += 5

        # check for collisions with platforms
        for platform in platforms:
            if player.y + 10 > platform.y and player.y < platform.y + platform.h and player.x > platform.x and player.x < platform.x + platform.w:
                player.y = platform.y

        # draw frame
        window.fill((0, 0, 0))

        # draw platforms
        for platform in platforms:
            pygame.draw.rect(window, (255, 255, 255), (platform.x, platform.y, platform.w, platform.h))

        # draw player
        pygame.draw.rect(window, (255, 255, 255), (player.x, player.y, 10, 10))

        pygame.display.update()
        clock.tick(60)
    except Exception as e:
        print(e)


