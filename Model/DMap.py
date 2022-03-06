# import the pygame module, so you can use it
import pickle
import pygame
import time

from pygame.locals import *
from random import random, randint
import numpy as np

BLUE = (0, 0, 255)
VIOLET = (136, 77, 109)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class DMap:

    def __init__(self):
        self.__n = 20
        self.__m = 20
        self.__surface = np.zeros((self.__n, self.__m))
        for i in range(self.__n):
            for j in range(self.__m):
                self.__surface[i][j] = -1

    def getN(self):
        return self.__n

    def getM(self):
        return self.__m

    def getSurface(self):
        return self.__surface



    def validCoordinates(self, x, y):
        return 0 <= x < self.__n and 0 <= y < self.__m

    def getValue(self, x, y):
        if not self.validCoordinates(x, y):
            raise Exception(" The current coordinates are not valid")
        return self.__surface[x][y]

    def image(self, x, y):

        imagine = pygame.Surface((420, 420))
        brick = pygame.Surface((20, 20))
        empty = pygame.Surface((20, 20))
        empty.fill(WHITE)
        brick.fill(BLACK)
        imagine.fill(VIOLET)

        for i in range(self.__n):
            for j in range(self.__m):
                if self.__surface[i][j] == 1:
                    imagine.blit(brick, (j * 20, i * 20))
                elif self.__surface[i][j] == 0:
                    imagine.blit(empty, (j * 20, i * 20))

        drona = pygame.image.load("../drona.png")
        imagine.blit(drona, (y * 20, x * 20))
        return imagine