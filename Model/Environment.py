# import the pygame module, so you can use it
import pickle
import pygame
import time

from pygame.locals import *
from random import random, randint
import numpy as np

# Creating some colors
DARKBLUE = (49, 70, 87)
GRAYBLUE = (50, 120, 120)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Environment:
    def __init__(self):
        self.__n = 20
        self.__m = 20
        self.__surface = np.zeros((self.__n, self.__m))

    def getN(self):
        return self.__n

    def getM(self):
        return self.__m

    def isCorrectlyPlaced(self, x, y):

        print(str(self.__surface[x][y]))
        print("The drone was initially placed on a field which has the value: " + str(self.__surface[x][y]))
        if self.__surface[x][y] == 1:
            raise Exception("The drone was initially placed on a wall")
        return True

    def randomMap(self, fill=0.2):
        for i in range(self.__n):
            for j in range(self.__m):
                if random() <= fill:
                    self.__surface[i][j] = 1

    def getSurface(self):
        return self.__surface


    def saveEnvironment(self, numFile):
        with open(numFile, 'wb') as f:
            pickle.dump(self, f)
            f.close()

    def loadEnvironment(self, numFile):
        with open(numFile, "rb") as f:
            dummy = pickle.load(f)
            self.__n = dummy.__n
            self.__m = dummy.__m
            self.__surface = dummy.__surface
            f.close()

    def image(self):
        imagine = pygame.Surface((420, 420))
        brick = pygame.Surface((20, 20))
        brick.fill(DARKBLUE)
        imagine.fill(WHITE)
        for i in range(self.__n):
            for j in range(self.__m):
                if self.__surface[i][j] == 1:
                    imagine.blit(brick, (j * 20, i * 20))

        return imagine

    def __str__(self):
        string = ""
        for i in range(self.__n):
            for j in range(self.__m):
                string = string + str(int(self.__surface[i][j]))
            string = string + "\n"
        return string
