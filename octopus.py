# octopus.py
# experimental game code for game jam
# created 3/3/2017 by Connor Dale

import sys, pygame, math, ctypes, imageList, random
from pygame.locals import*

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
		self.speed = [0,0]
		self.jump_speed = -4

	def move(self):
		self.x += self.speed[0]
		self.y += self.speed[1]
		if self.speed[1] == self.jump_speed or self.speed[1] == 2: # octopus is jumping or hitting the ceiling
			self.speed[1] = 1 # gravity
		elif self.y >= self.floor: # octopus is hitting the floor
			self.speed[1] = 0

		# update Rect object position
		self.rect[0] = self.x
		self.rect[1] = self.y

	def draw(self,surface):
		surface.blit(self.image, (self.x, self.y))


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def swimAround():
	'''
	Creates a pygame window with a user-controlled octopus that can move left, right, and up
	'''
	pygame.init()

	# create game window
	white = (255, 255, 255) # color of background
	screen = pygame.display.set_mode((0,0),FULLSCREEN)
	size = screen.get_size()

	# create octopus object
	octy = Octopus(size)
	print(size)

	iters = 0
	max_iters = 20 # used for animating movement -- image changes every 20 iterations
	while True:
		screen.fill(white) # fill background

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
			octy.speed[0] = -2
			octy.image = octy.leftImages.current.data
		elif pressedKeys[pygame.K_RIGHT]: # Move right
			octy.speed[0] = 2
			octy.image = octy.rightImages.current.data
		else: # Stand still
			octy.speed[0] = 0

		if pressedKeys[pygame.K_UP]: # Jump upwards
			octy.speed[1] = octy.jump_speed

		# check for collisions with the edges of the window
		if octy.x <= 0:
			octy.speed[0] = 2
		elif octy.x + octy.rect[2] >= size[0]:
			octy.speed[0] = -2
		if octy.y <= 0:
			octy.speed[1] = 2
		elif octy.y + octy.rect[3] >= size[1]:
			octy.speed[1] = -2
		
		# move the octopus
		octy.move()

		# draw the octopus in the window
		octy.draw(screen)

		# change image for animation
		if iters == max_iters:
			octy.leftImages.update_current()
			octy.rightImages.update_current()
			iters = 0
		else:
			iters += 1

		pygame.display.flip()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def main():
	## this is an octopus that moves around the screen
	swimAround()

if __name__=="__main__":
	main()
