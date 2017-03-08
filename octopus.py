# octopus.py
# experimental game code for game jam
# created 3/3/2017 by Connor Dale

import sys, pygame, math, ctypes, imageList, random
from levels import LEVELS_SPEC
from pygame.locals import*


# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

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
		self.image = self.rightImages.current.data # image that is displayed
		self.rect = self.image.get_rect() # rect used for collision detection
		
		self.floor = win_size[1]-self.rect[3]-1

		# set starting position
		self.x = int(win_size[0]/2) # octopus starts halfway across the screen
		self.y = self.floor # octopus starts at the bottom of the screen
		
		# set rect coordinates to match image position
		self.rect[0] = self.x
		self.rect[1] = self.y

		# set starting speed (stationary)
		self.speed = [15,0]
		self.jump_speed = -10

	def move(self):
		# self.x += self.speed[0]
		self.y += self.speed[1]
		if self.speed[1] == self.jump_speed or self.speed[1] == 2: # octopus is jumping or hitting the ceiling
			self.speed[1] = 10 # gravity
		elif self.y >= self.floor: # octopus is hitting the floor
			self.speed[1] = 0

		# update Rect object position
		self.rect[0] = self.x
		self.rect[1] = self.y
		# if self.rect.colliderect()

	def move_left(self):
		# self.speed[0] = 20
		self.x-=self.speed[0]

	def move_right(self):
		# self.speed[0] = 20
		self.x+=self.speed[0]

	def draw(self,surface):
		surface.blit(self.image, (self.x, self.y))


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Platform(pygame.sprite.Sprite):
	""" Platform the user can jump on """
 
	def __init__(self, width, height):
		""" Platform constructor. Assumes constructed with user passing in
			an array of 5 numbers like what's defined at the top of this code.
			"""
		super().__init__()
 
		self.image = pygame.Surface([width, height])
		self.image.fill(GREEN)
 
		self.rect = self.image.get_rect()

class Level():
	""" This is a generic super-class used to define a level.
		Create a child class for each level with level-specific
		info. """
 
	def __init__(self, player, level_spec):
		""" Constructor. Pass in a handle to player. Needed for when moving
			platforms collide with the player. """
		self.platform_list = pygame.sprite.Group()
		self.enemy_list = pygame.sprite.Group()
		self.player = player
 
		# How far this world has been scrolled left/right
		self.world_shift = 0
 
		self.level_limit = -1000
 
		# Go through the array above and add platforms
		for block in level_spec:
			self.platform_list.add(block)
 
	# Update everythign on this level
	def update(self):
		""" Update everything in this level."""
		self.platform_list.update()
		self.enemy_list.update()
 
	def draw(self, screen):
		""" Draw everything on this level. """
 
		# Draw all the sprite lists that we have
		self.platform_list.draw(screen)
		self.enemy_list.draw(screen)
 
	def shift_world(self, shift_x):
		""" When the user moves left/right and we need to scroll
		everything: """
 
		# Keep track of the shift amount
		self.world_shift += shift_x
 
		# Go through all the sprite lists and shift
		for platform in self.platform_list:
			platform.rect.x += shift_x
 
		for enemy in self.enemy_list:
			enemy.rect.x += shift_x
 

def swimAround():
	'''
	Creates a pygame window with a user-controlled octopus that can move left, right, and up
	'''
	pygame.init()

	bg = pygame.image.load("images/testbg.jpg")
	size = bg.get_size()
	bg_rect = bg.get_rect()
	screen = pygame.display.set_mode(size)
	w,h = size
	x = 0
	y = 0
	x1 = w
	y1 = 0
	# create game window
	# white = (255, 255, 255) # color of background
	# screen = pygame.display.set_mode((0,0),FULLSCREEN)
	# size = screen.get_size()

	# create octopus object
	octy = Octopus(size)

	level_list = [Level(octy, spec) for spec in LEVELS_SPEC]
	curent_level_no = 0
	current_level = level_list[curent_level_no]
	active_sprite_list = pygame.sprite.Group()
	octy.level = current_level

	# active_sprite_list.add(octy)

	clock = pygame.time.Clock()
	iters = 0
	max_iters = 3 # used for animating movement -- image changes every 20 iterations
	while True:
		# check for events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit() 
				sys.exit()
	
		pressedKeys = pygame.key.get_pressed()

		if pressedKeys[pygame.K_ESCAPE]: # Exit
			pygame.quit()
			sys.exit()
		elif pressedKeys[pygame.K_LEFT]: # Move left
			# octy.speed[0] = -2
			octy.move_left()
			octy.image = octy.leftImages.current.data
		elif pressedKeys[pygame.K_RIGHT]: # Move right
			# octy.speed[0] = 2
			octy.move_right()
			octy.image = octy.rightImages.current.data
		# else: # Stand still
			# octy.speed[0] = 0

		if pressedKeys[pygame.K_UP]: # Jump upwards
			octy.speed[1] = octy.jump_speed

		# check for collisions with the edges of the window
		if octy.x <= int(.1*size[0]):
			octy.move_right()
			diff = octy.rect[2]
			current_level.shift_world(octy.speed[0])
			x1 += octy.speed[0]
			x += octy.speed[0]
			if x > w:
				x = -w
			if x1 > w:
				x1 = -w
		elif octy.x + octy.rect[2] >= int(.9*size[0]):
			octy.move_left()
			diff = octy.rect[2]
			current_level.shift_world(-octy.speed[0])
			x1 -= octy.speed[0]
			x -= octy.speed[0]
			if x < -w:
				x = w
			if x1 < -w:
				x1 = w

		if octy.y <= 0:
			octy.speed[1] = 2
		elif octy.y + octy.rect[3] >= size[1]:
			octy.speed[1] = -2
		
		active_sprite_list.update()
		current_level.update()

		# move the octopus
		octy.move()

		# draw the background
		screen.blit(bg,(x,y))
		screen.blit(bg,(x1,y1))

		# change octopus image for animation
		if iters == max_iters:
			octy.leftImages.update_current()
			octy.rightImages.update_current()
			iters = 0
		else:
			iters += 1

		# draw the octopus and other objects
		current_level.draw(screen)
		active_sprite_list.draw(screen)
		octy.draw(screen)

		clock.tick(60)

		pygame.display.flip()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def main():
	## this is an octopus that moves around the screen
	swimAround()

if __name__=="__main__":
	main()
