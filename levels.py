import pygame


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)



# DumbWall(x, y, width, height),
# DangerWall(x, y, width, height),
# DangerWall(x, y, width, height),
# Collectible('CRAB', x, y), # width and height will be a default size
# Garden(x=1000)  # only needs x position

class _wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class DumbWall(_wall):
    "Wall that blocks passage"
    def collision_detected(self):
        print("Collided with Dumbwall")


class DangerWall(_wall):
    "Wall that kills the octopus"
    def collision_detected(self):
        print("Collided with Dangerwall")


class Collectible(pygame.sprite.Sprite):
    width = height = 20

    def __init__(self, name, x, y):
        super().__init__()
        # TODO: choose an image based on the name
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def collision_detected(self):
        print("Just got a collectible")

class Garden(pygame.sprite.Sprite):
    height = 1000  # TODO: screen height
    width = 10

    def __init__(self, x):
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.y = 0
        self.rect.x = x
        super().__init__()

    def collision_detected(self):
        print("Now inside the garden")

WIDTH, HEIGHT = 1920, 1080


LEVELS_SPEC = [
    [
        DumbWall(200, 200, 10, HEIGHT - 200),
        DumbWall(500, 200, 10, HEIGHT - 200),
        DangerWall(600, 0, 10, HEIGHT - 200),
        Collectible('crab', 1000, HEIGHT - Collectible.height),
        DangerWall(1200, 200, 10, HEIGHT - 200),
        Collectible('crab', 1600, HEIGHT - Collectible.height),
        DangerWall(1800, 0, 10, HEIGHT - 200),
        Garden(1920),
    ],
    # next levels go here
]
