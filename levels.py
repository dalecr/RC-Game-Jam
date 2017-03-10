import pygame


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class _wall(pygame.sprite.Sprite):
    is_fixed = True
    is_killer = False
    is_end = False
    color = BLACK

    def __init__(self, x, y, width=40, height=440):
        super().__init__()
        self.image = pygame.Surface([width, height])
        tile = pygame.image.load(self.pic)
        for i in range(0, height, 40):
            self.image.blit(tile, (0, i))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def is_fixed(self):
        return True


class DumbWall(_wall):
    "Wall that blocks passage"

    pic = 'images/dumbwall.png'
    # pic = 'images/dangerwall.png'
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
    is_end = True

    def __init__(self, x):
        self.image = pygame.image.load("images/garden.png")

        self.rect = self.image.get_rect()
        self.rect.y = 0
        self.rect.x = x
        super().__init__()

    def collision_detected(self):
        print("Now inside the garden")


WIDTH, HEIGHT = 1200, 700


def height_from_bottom(x):
    return HEIGHT - Collectible.height - x


LEVELS_SPEC = [

    [
        # first level
        Collectible('crab', 200, height_from_bottom(250)),
        Collectible('crab', 200, height_from_bottom(150)),
        Collectible('crab', 200, height_from_bottom(50)),
        Collectible('crab', 750, 50),
        DumbWall(800, 250),
        Collectible('crab', 900, 50),
        Collectible('crab', 1050, 50),
        Collectible('crab', 1180, 50),
        Collectible('crab', 1000, height_from_bottom(450)),
        Collectible('crab', 1000, height_from_bottom(350)),
        Collectible('crab', 1000, height_from_bottom(250)),
        Collectible('crab', 1000, height_from_bottom(150)),
        Collectible('crab', 1000, height_from_bottom(50)),
        DumbWall(1200, 250),

        Collectible('crab', 1450, 350),
        Collectible('crab', 1450, 250),
        Collectible('crab', 1450, 150),
        Collectible('crab', 1450, 50),
        Collectible('crab', 1580, height_from_bottom(150)),
        Collectible('crab', 1580, height_from_bottom(50)),
        DangerWall(1600, 0),
        Collectible('crab', 1650, 50),
        Collectible('crab', 1650, 100),
        Collectible('crab', 1650, 150),
        Collectible('crab', 1700, 50),
        Collectible('crab', 1700, 100),
        Collectible('crab', 1700, 150),

        Collectible('crab', 2000, height_from_bottom(350)),
        Collectible('crab', 2000, height_from_bottom(250)),
        Collectible('crab', 2000, height_from_bottom(150)),
        Collectible('crab', 2000, height_from_bottom(50)),
        Collectible('crab', 2120, 50),
        Collectible('crab', 2120, 150),
        DangerWall(2150, 250),

        Collectible('crab', 2350, 50),
        Collectible('crab', 2350, 150),
        Collectible('crab', 2350, 250),
        Collectible('crab', 2350, 350),
        Collectible('crab', 2500, 50),
        Collectible('crab', 2500, 150),
        Collectible('crab', 2500, 250),
        Collectible('crab', 2500, 350),
        DangerWall(2650, 250),

        Collectible('crab', 3200, height_from_bottom(150)),
        Collectible('crab', 3200, height_from_bottom(50)),
        DangerWall(3200, 0),

        Garden(3600),
    ],
    [
        # second level
        Collectible('crab', 200, height_from_bottom(250)),
        Collectible('crab', 200, height_from_bottom(150)),
        Collectible('crab', 200, height_from_bottom(50)),
        Collectible('crab', 780, 300),
        Collectible('crab', 780, 360),
        DangerWall(800, 0, height=240),
        DangerWall(800, 500),

        Collectible('crab', 1000, HEIGHT - Collectible.height - 50),
        DangerWall(1200, 250),
        Collectible('crab', 1150, 50),

        Collectible('crab', 1300, height_from_bottom(50)),
        Collectible('crab', 1300, height_from_bottom(150)),

        Collectible('crab', 1580, 300),
        Collectible('crab', 1580, 360),
        DangerWall(1600, 0, height=240),
        DangerWall(1600, 500),

        Collectible('crab', 1700, 50),
        Collectible('crab', 1700, 150),

        Collectible('crab', 1700, HEIGHT - Collectible.height - 50),
        Collectible('crab', 2000, HEIGHT - Collectible.height - 50),
        DangerWall(2200, 250),

        Collectible('crab', 2450, 50),
        Collectible('crab', 2450, 150),
        Collectible('crab', 2550, 50),
        Collectible('crab', 2550, 150),
        Collectible('crab', 2650, 50),
        Collectible('crab', 2650, 150),
        DangerWall(2800, 0),
        Garden(3600),
    ],
    [
        Collectible('crab', 200, height_from_bottom(300)),
        DangerWall(800,0,height=240),
        Collectible('crab', 800, 300),
        Collectible('crab', 800, 400),
        DangerWall(800,500),
        DangerWall(900,0,height=300),
        DangerWall(900,520),
        Collectible('crab', 900, 300),
        Collectible('crab', 900, 400),
        DangerWall(1000,0,height=240),
        DangerWall(1000,600),
        Collectible('crab', 1000, 300),
        Collectible('crab', 1000, 400),
        DangerWall(1100,0,height=300),
        DangerWall(1100,500),
        Collectible('crab', 1180, height_from_bottom(50)),
        Collectible('crab', 1180, height_from_bottom(150)),
        Collectible('crab', 1180, height_from_bottom(250)),
        Collectible('crab', 1180, height_from_bottom(350)),
        Collectible('crab', 1180, height_from_bottom(450)),
        Collectible('crab', 1180, height_from_bottom(550)),
        Collectible('crab', 1180, height_from_bottom(650)),
        DangerWall(1300,0,height=400),
        DangerWall(1300,650),
        Collectible('crab', 1410, height_from_bottom(50)),
        Collectible('crab', 1410, height_from_bottom(150)),
        Collectible('crab', 1410, height_from_bottom(250)),
        Collectible('crab', 1410, height_from_bottom(350)),
        Collectible('crab', 1410, height_from_bottom(450)),
        Collectible('crab', 1410, height_from_bottom(550)),
        Collectible('crab', 1410, height_from_bottom(650)),
        DangerWall(1600,400),
        Collectible('crab', 1710, height_from_bottom(50)),
        Collectible('crab', 1710, height_from_bottom(150)),
        Collectible('crab', 1710, height_from_bottom(250)),
        Collectible('crab', 1710, height_from_bottom(350)),
        Collectible('crab', 1710, height_from_bottom(450)),
        Collectible('crab', 1710, height_from_bottom(550)),
        Collectible('crab', 1710, height_from_bottom(650)),
        DangerWall(1850,0,height=400),
        Collectible('crab', 2010, height_from_bottom(50)),
        Collectible('crab', 2010, height_from_bottom(150)),
        Collectible('crab', 2010, height_from_bottom(250)),
        Collectible('crab', 2010, height_from_bottom(350)),
        Collectible('crab', 2010, height_from_bottom(450)),
        Collectible('crab', 2010, height_from_bottom(550)),
        Collectible('crab', 2010, height_from_bottom(650)),
        Garden(2400)
    ],
]
