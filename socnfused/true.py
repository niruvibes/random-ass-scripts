import pygame
from pygame.locals import *
import sys

# initialize pygame
pygame.init()

# create the game window
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Platformer")
print("Window created")

# create the game clock
clock = pygame.time.Clock()

 # create the player character
class Player:
    def __init__(self, x, y, margin=1):  # <-- add the `margin` argument here, with a default value of `1`
        self.x = x
        self.y = y
        self.speed = 5
        self.jumping = False
        self.jump_speed = 10
        self.jump_time = 0
        self.margin = margin  # <-- assign the `margin` argument to `self.margin`

class Platform:
    def __init__(self, x, y, w, h, margin=1):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.margin = 1  # <-- define `margin` as `self.margin`


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
        if (keys[K_LEFT] or keys[K_a]) and player.x > 0:
            player.x -= player.speed
        if (keys[K_RIGHT] or keys[K_d])and player.x < 800 - 10:
            player.x += player.speed

        # check for collisions with platforms
        for platform in platforms:
            # check if the player's x position is within the x range of the platform
            if player.x + player.margin + 10 > platform.x and player.x - player.margin < platform.x + platform.w:
                # check if the player's y position is within the y range of the platform
                if player.y + player.margin + 10 > platform.y and player.y - player.margin < platform.y + platform.h:
                    # only set the player's y position to the top of the platform if the player is moving down
                    if player.y < platform.y:
                        player.y = platform.y - player.margin - 10  # set the player's y position to the top of the platform, minus the player's margin
                        player.jumping = False  # stop the player from jumping when they land on a platform

        # handle jumping
        if (keys[K_SPACE] or keys[K_w]) and not player.jumping:
            # only start a new jump if the player is not already jumping
            # and if the player is standing on a platform
            on_platform = False
            for platform in platforms:
                if player.y + player.margin + 10 > platform.y and player.y - player.margin < platform.y + platform.h:
                    on_platform = True
                    break
            if on_platform:
                player.jumping = True
                player.jump_time = 10
        if player.jumping:
            player.y -= player.jump_speed
            player.jump_time -= 1
            if player.jump_time == 0:
                player.jumping = False

        # apply gravity if the player is not standing on a platform
        if player.jumping or player.y + player.margin + 10 < min([platform.y for platform in platforms]):
            player.y += 5


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


