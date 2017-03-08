#!/usr/bin/python

'''
'''
import sys, pygame, math, ctypes, imageList, random
from pygame.locals import*

class Enemy(pygame.sprite.Sprite):


    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pygame.image.load("images/enemy.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect() # rect used for collision detection
        self.rect[0] = self.x
        self.rect[1] = self.y

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def collision_happened(self):
        print("Collision detected")

    def move(self):
            self.x += 5
            self.y += 5
            # update Rect object position
            self.rect[0] = self.x
            self.rect[1] = self.y
