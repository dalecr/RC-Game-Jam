# octopus.py
# experimental game code for game jam
# created 3/3/2017 by Connor Dale
 
import sys, pygame, imageList
from levels import LEVELS_SPEC
from pygame.locals import*


class welcome(object):
    def __init__(self,win):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.image.load("images/start.png")
       win.blit(self.image,(200,0))


class death(object):

    def __init__(self,win, octopus):
        pygame.sprite.Sprite.__init__(self)
        self.images = imageList.CircularLinkedList()

        for i in range(4) :
            dirname = "images/you_died/"
            img = dirname + "dead-" + str(i) + ".png"
            self.images.append(pygame.image.load(img))

        self.images.set_current()
        self.image = self.images.current.data # image that is displayed

        self.x = int(win.get_size()[0]/2 - self.image.get_rect()[2]/2)#octopus.x
        self.y = int(win.get_size()[1]/2 - self.image.get_rect()[3]/2)#octopus.y
        self.playedSound = False;

    def draw(self,surface,octopus):
        # draws the octopus on the given surface
        self.images.update_current()
        self.image = self.images.current.data
        surface.blit(self.image, (self.x, self.y))
        self.play()
        self.kill(octopus)

    def play(self):
        if self.playedSound == False:
            sfx = ['supermario.mp3','wilhelm_scream.mp3']
            import random
            mp3 = random.choice(sfx) 
            pygame.mixer.music.load("sfx/" + mp3)
            pygame.mixer.music.play(0)
            self.playedSound = True

    def kill(self,octopus):
        if(self.playedSound == True):
            for i in range(3) :
                dirname = "images/you_died/"
                imgName = dirname + "deado-" + str(i) + ".png"
                img = pygame.image.load(imgName)
                img = pygame.transform.rotate(img,180)
                
                octopus.leftImages.append(img);


        octopus.image = octopus.leftImages.current.data # image that is displayed
        octopus.rect = octopus.image.get_rect() # rect used for collision detection


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class Octopus(object):

    def __init__(self,win_size):
        pygame.sprite.Sprite.__init__(self)

        # set separate images for moving left/right
        # populate a circular linked list with image objects
        #  they can be cycled-through as the octopus moves to animate it
        self.leftImages = imageList.CircularLinkedList()
        self.leftImages.append(pygame.image.load("images/octopus_l.png"))
        self.leftImages.append(pygame.image.load("images/octopus_l2.png"))
        self.leftImages.set_current() # sets a 'current image' marker on the last image in the list
        self.rightImages = imageList.CircularLinkedList()
        self.rightImages.append(pygame.image.load("images/octopus_r.png"))
        self.rightImages.append(pygame.image.load("images/octopus_r2.png"))
        self.rightImages.set_current()
        # self.jump_image = pygame.image.load("images/octopus_jump.png")
        self.image = self.rightImages.current.data # image that is displayed
        self.rect = self.image.get_rect() # rect used for collision detection
        self.image_list = self.rightImages

        self.floor = win_size[1]-self.rect[3]

        # set starting position
        self.x = int(win_size[0]*.15) # octopus starts on the left side of the screen
        self.y = 15 # octopus starts at the top of the screen

        # set rect coordinates to match image position
        self.rect[0] = self.x
        self.rect[1] = self.y

        # set starting speed (stationary)
        self.speed = [11,11]
        self.jump_speed = -18

        self.blocked = None
        self.dead = False

    def fall(self):
        # moves the octopus downwards/upwards and updates its vertical speed and rect
        self.y += self.speed[1]
        if self.y >= self.floor: # octopus is hitting the floor
            self.speed[1] = 0
            self.y = self.floor - 2
        else:
            self.speed[1] = 11 # gravity

        if GAME_STATE.game_over:
            self.speed[1] = -1
        # update Rect object position
        self.rect[0] = self.x
        self.rect[1] = self.y

    def move_left(self):
        # moves the octopus left and updates its rect
        self.x-=self.speed[0]
        self.rect[0] = self.x
        self.rect[1] = self.y

    def move_right(self):

        self.x+=self.speed[0]
        self.rect[0] = self.x
        self.rect[1] = self.y

    def draw(self,surface):
        # draws the octopus on the given surface
        surface.blit(self.image, (self.x, self.y))


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class Level():
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    def __init__(self, player, level_spec):
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.collectible_list = pygame.sprite.Group()
        self.killer_list = pygame.sprite.Group()
        self.level_spec = level_spec

        # How far this world has been scrolled left/right
        self.world_shift = 0

        self.level_limit = -1000

        # Go through the array above and add platforms
        for block in level_spec:
            if block.is_killer:
                self.killer_list.add(block)
            elif block.is_fixed:
                self.platform_list.add(block)
            else:
                self.collectible_list.add(block)

    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.collectible_list.update()
        self.killer_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.collectible_list.draw(screen)
        self.killer_list.draw(screen)


    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll
        everything: """

        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x
        for wall in self.killer_list:
            wall.rect.x += shift_x
        for enemy in self.collectible_list:
            enemy.rect.x += shift_x

    def detect_collisions(self, thing):

        if pygame.sprite.spritecollideany(thing, self.killer_list, False):
            GAME_STATE.game_over = True

        collision_list = pygame.sprite.spritecollide(thing, self.platform_list, False)
        wall_parameters = ()
        for collision in collision_list:
            collision.collision_detected()
            if collision.is_end:
                GAME_STATE.current_level_index += 1
                GAME_STATE.finished = True

            wall_parameters = (collision.rect.top, collision.rect.left + collision.rect.width, collision.rect.top + collision.rect.height, collision.rect.left)
            # print(wall_parameters)

        collision_list = pygame.sprite.spritecollide(thing, self.collectible_list, True)
        for collision in collision_list:
            collision.collision_detected()
            GAME_STATE.score += 1

        if wall_parameters:
            return wall_parameters
        else:
            return None


class GameState():
    score = 0
    current_level_index = 0
    end_level = 0
    finished = True
    game_over = False
    start_screen = True



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def draw_score(screen, score, level):
    score_font = pygame.font.Font('freesansbold.ttf', 30)
    score_surf = score_font.render('Score: %s' % score, True, (255, 255,255))
    level_surf = score_font.render('Level: %s' % level, True, (255, 255,255))
  
    score_rect = score_surf.get_rect()
    score_rect.topleft = (50, 50)
  
    level_rect = level_surf.get_rect()
    level_rect.topleft = (50, 150)
  
    screen.blit(score_surf, score_rect)
    screen.blit(level_surf, level_rect)


GAME_STATE = GameState()


def next_level(screen):
    # create octopus and death objects
    octy = Octopus(screen.get_size())
    d = death(screen, octy)

    level_list = [Level(octy, spec) for spec in LEVELS_SPEC]
    current_level = level_list[GAME_STATE.current_level_index]

    return octy,d,current_level


def run_game():
    '''
    Creates a pygame window with a user-controlled octopus that can move left, right, and up
    '''
    pygame.init()

    bg = pygame.image.load("images/undersea.png")
    size = bg.get_size()
    bg_rect = bg.get_rect()
    screen = pygame.display.set_mode(size)
    w,h = size

    clock = pygame.time.Clock()
    iters = 0
    max_iters = 3 # used for animating movement -- image changes every max_iters iterations
    while True:
        if GAME_STATE.start_screen:
            screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    GAME_STATE.start_screen = False
            welcome(screen)
            pygame.display.flip()
            continue

        if GAME_STATE.finished:
            octy,d,current_level = next_level(screen)
            x = 0
            y = 0
            x1 = w
            y1 = 0
            GAME_STATE.finished = False

        # check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pressedKeys = pygame.key.get_pressed()

        if pressedKeys[pygame.K_ESCAPE]: # Exit
            pygame.quit()
            sys.exit()
        if not GAME_STATE.game_over:
            if pressedKeys[pygame.K_LEFT]: # Move left
                octy.move_left()
                octy.image = octy.leftImages.current.data
                octy.image_list = octy.leftImages
            elif pressedKeys[pygame.K_RIGHT]: # Move right
                octy.move_right()
                octy.image = octy.rightImages.current.data
                octy.image_list = octy.rightImages
            if pressedKeys[pygame.K_UP]: # Jump upwards
                octy.speed[1] = octy.jump_speed
                octy.image = octy.image_list.current.data


        # check for collisions with the edges of the window
        if octy.x <= int(.1*size[0]):
            octy.move_right()
            current_level.shift_world(octy.speed[0])
            x1 += octy.speed[0]
            x += octy.speed[0]
            if x > w:
                x = -w
            if x1 > w:
                x1 = -w
        elif octy.x + octy.rect[2] >= int(.8*size[0]):
            octy.move_left()
            current_level.shift_world(-octy.speed[0])
            x1 -= octy.speed[0]
            x -= octy.speed[0]
            if x < -w:
                x = w
            if x1 < -w:
                x1 = w

        if octy.y < 0:
            octy.speed[1] = 2
            octy.y = 2

        current_level.update()

        # move the octopus
        octy.fall()

        # change octopus image for animation
        if iters == max_iters:
            octy.leftImages.update_current()
            octy.rightImages.update_current()
            iters = 0
        else:
            iters += 1


        # return parameters of wall if blocked
        octy.blocked = current_level.detect_collisions(octy)


        #change position if blocked by wall
        if octy.blocked:
            if pressedKeys[pygame.K_LEFT]: # bounce back right
                octy.x += 10
                octy.move_right()
            elif pressedKeys[pygame.K_RIGHT]:
                octy.x -= 10
                octy.move_left()
            octy.speed[1] = 0

        # draw the background
        screen.blit(bg,(x,y))
        screen.blit(bg,(x1,y1))

        # draw the octopus and other objects
        current_level.draw(screen)
        octy.draw(screen)
        draw_score(screen, GAME_STATE.score, GAME_STATE.current_level_index + 1)

        if GAME_STATE.game_over:
            d.draw(screen, octy)

            # if pressedKeys[pygame.K_r]: # restart game
            #     GAME_STATE.finished = True
            #     GAME_STATE.game_over = False
            #     pygame.quit()
            #     return True

        clock.tick(60)

        pygame.display.flip()


def main():
    replay = True
    while replay:
        replay = run_game()

if __name__=="__main__":
    main()
