# kraken.py
# experimental game code for game jam
# created 3/3/2017 by Connor Dale

import sys, pygame, math, ctypes, imageList, random
from pygame.locals import*

class Hero(object):

	def __init__(self,win_size):
		pygame.sprite.Sprite.__init__(self)

		# set separate images for moving left/right
		self.leftImages = imageList.CircularLinkedList()
		self.leftImages.append(pygame.image.load("images/hero_l.png"))
		self.leftImages.set_current()
		self.rightImages = imageList.CircularLinkedList()
		self.rightImages.append(pygame.image.load("images/hero_r.png"))
		self.rightImages.set_current()
		# self.jumpImage = pygame.image.load("images/herojump.png")
		self.image = self.rightImages.current.data
		self.rect = self.image.get_rect() # rect used for collision detection
		
		self.floor = win_size[1]-self.rect[3]-2

		# set starting position
		self.x = int(win_size[0]/2)
		self.y = self.floor
		self.rect[0] = self.x
		self.rect[1] = self.y

		# set starting speed (stationary)
		self.speed = [0,0]
		self.jump_speed = -21
		self.jump = False

	def move(self):
		self.x += self.speed[0]
		self.y += self.speed[1]
		if self.jump:
			if self. speed[1] != 0:
				self.speed[1] += 2
			else: 
				self.jump = False
		self.rect[0] = self.x
		self.rect[1] = self.y

	def draw(self,surface):
		surface.blit(self.image, (self.x, self.y))


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class Arm(object):

	def __init__(self,win_size):
		pygame.sprite.Sprite.__init__(self)

		# use list to store starting positions and images
		# use random to choose list index of starting position and corresponding image
		# arms will appear semi-randomly on the screen

		i = random.randint(0,3)

		# populate a circular linked list with image objects
		#  they can be cycled-through as the arm moves to animate it
		right_images = imageList.CircularLinkedList()
		# right_images.append(pygame.image.load("images/arm_r.png"))
		# right_images.append(pygame.image.load("images/arm_r2.png"))
		right_images.append(pygame.image.load("images/arm_r.png"))
		right_images.append(pygame.image.load("images/arm_r3.png"))
		left_images = imageList.CircularLinkedList()
		# left_images.append(pygame.image.load("images/arm_l.png"))
		# left_images.append(pygame.image.load("images/arm_l2.png"))
		left_images.append(pygame.image.load("images/arm_l.png"))
		left_images.append(pygame.image.load("images/arm_l3.png"))
		
		images = (left_images,right_images)
		self.images = images[i%2]
		self.images.set_current()

		self.rect = self.images.current.data.get_rect()

		# for falling arms
		# starts = ((0,-self.rect[3]),(win_size[0]-self.rect[2],-self.rect[3]))

		# for pushing arms
		starts = ((-self.rect[2],int(win_size[1]*.25)),(win_size[0],int(win_size[1]*.25)),
					(-self.rect[2],int(win_size[1]*.75)),(win_size[0],int(win_size[1]*.75)))
		speeds = ([2,0],[-2,0])

		self.x = starts[i][0]
		self.y = starts[i][1]
		self.rect[0] = self.x
		self.rect[1] = self.y
		
		self.speed = speeds[i%2] #(0,2)

	def move(self,win_size):
		# self.y += self.speed[1]
		if (self.x + 2 < 0) or (self.x - 2 > win_size[0] - self.rect[2]):
			self.x += self.speed[0]
		else:
			self.speed[0] = -self.speed[0]
			self.x += self.speed[0]
		self.rect[0] = self.x
		self.rect[1] = self.y

	def draw(self,surface):
		surface.blit(self.images.current.data, (self.x, self.y))

		
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def releaseTheKraken():
	'''
	player controlls a hero, giant octopus arms push the hero around
	-- basically Clash of the Titans
	'''
	pygame.init()

	# create game window
	white = (255, 255, 255) # color of background
	screen = pygame.display.set_mode((0,0),FULLSCREEN)
	size = screen.get_size()

	# create game window
	white = (255, 255, 255)
	screen = pygame.display.set_mode((0,0),FULLSCREEN)

	# create hero and arm objects
	hero = Hero(size)
	arm = Arm(size)
	
	iters = 0
	max_iters = 40 # used for animations
	while True:
		screen.fill(white) # fill screen
		
		# update images for animation
		if iters == max_iters:
			arm.images.update_current()
			# arms.append(Arm(size))

		# check for events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit() 
				sys.exit()

			pressedKeys = pygame.key.get_pressed()

			if pressedKeys[pygame.K_ESCAPE]: # Exit
				pygame.quit()
				sys.exit()
			elif pressedKeys[pygame.K_LEFT]: # move left
				hero.speed[0] = -2
				hero.image = hero.leftImages.current.data
			elif pressedKeys[pygame.K_RIGHT]: # move right
				hero.speed[0] = 2
				hero.image = hero.rightImages.current.data
			else: # stand still
				hero.speed[0] = 0

			if pressedKeys[pygame.K_UP]: # jump
				hero.jump = True
				hero.speed[1] = hero.jump_speed

		# check for collisions with arms
		if hero.rect.colliderect(arm.rect):
			hero.speed[0] = arm.speed[0]

		# check for collisions with the edges of the window
		if hero.x <= 0:
			hero.speed[0] = 2
		elif hero.x + hero.rect[2] >= size[0]:
			hero.speed[0] = -2
		if hero.y <= 0:
			hero.speed[1] = 2
		elif hero.y + hero.rect[3] >= size[1]:
			hero.speed[1] = -2

		# move everything
		hero.move()
		arm.move(size)

		# draw everything
		hero.draw(screen)
		arm.draw(screen)

		## replaces falling arms that have exited the window
		# if arm.y > size[1]:
		# 	arm = Arm(size)

		## replaces arms that have exited the window
		if (arm.x > size[0] + 5) or (arm.x < -arm.rect[2] -5):
			arm = Arm(size)

		iters += 1
		if iters > max_iters:
			iters = 0

		pygame.display.flip()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def main():
	## this is giant octopus arms that push the player around
	releaseTheKraken()

if __name__=="__main__":
	main()