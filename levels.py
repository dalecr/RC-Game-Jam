import pygame


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class _wall(pygame.sprite.Sprite):
    is_fixed = True
    is_killer = False

    def __init__(self, x, y, width=40, height=450):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image = pygame.image.load(self.pic)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def is_fixed(self):
        return True


class DumbWall(_wall):
    "Wall that blocks passage"

    pic = 'images/dumbwall.png'
    def collision_detected(self):
        print("Collided with Dumbwall")


class DangerWall(_wall):
    pic = 'images/dangerwall.png'
    is_killer = True
    "Wall that kills the octopus"
    def collision_detected(self):
        print("Collided with Dangerwall")


class Collectible(pygame.sprite.Sprite):
    width = height = 40
    is_fixed = False
    is_killer = False

    def __init__(self, name, x, y):
        super().__init__()
        # TODO: choose an image based on the name
        self.image = pygame.Surface([self.width, self.height])
        images = {"crab": 'images/crab.png'}
        self.image = pygame.image.load(images.get(name))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def collision_detected(self):
        print("Just got a collectible")


class Garden(pygame.sprite.Sprite):
    height = 1000  # TODO: screen height
    width = 10
    is_fixed = True
    is_killer = False

    def __init__(self, x):
        self.image = pygame.Surface([self.width, self.height])

        self.rect = self.image.get_rect()
        self.rect.y = 0
        self.rect.x = x
        super().__init__()

    def collision_detected(self):
        print("Now inside the garden")

WIDTH, HEIGHT = 1200, 700


LEVELS_SPEC = [
    [
        Collectible('crab', 100, HEIGHT - Collectible.height - 200),
        Collectible('crab', 100, HEIGHT - Collectible.height - 50),
        DumbWall(800, 250),
        DumbWall(1200, 250),
        DangerWall(1600, 0),
        Collectible('crab', 2000, HEIGHT - Collectible.height - 50),
        DangerWall(2200, 250),
        Collectible('crab', 1600, HEIGHT - Collectible.height - 50),
        DangerWall(2800, 0),
        Garden(3200),
    ],
    [
        Collectible('crab', 100, HEIGHT - Collectible.height - 200),
        Collectible('crab', 100, HEIGHT - Collectible.height - 50),
        DumbWall(800, 0, height=250),
        DumbWall(800, 500),
        DumbWall(1200, 250),
        DangerWall(1600, 0, height=250),
        DangerWall(1600, 500),
        Collectible('crab', 1700, HEIGHT - Collectible.height - 50),
        Collectible('crab', 2000, HEIGHT - Collectible.height - 50),
        DangerWall(2200, 250),
        DangerWall(2800, 0),
        Garden(3200),
    ],
]
