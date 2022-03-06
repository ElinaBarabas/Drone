# import the pygame module, so you can use it
import pickle
import pygame
import time

from pygame.locals import *
from random import random, randint
import numpy as np

# define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3


# define indexes variations
left_coordinates = [-1, 0]
up_coordinates = [0, 1]
right_coordinates = [1, 0]
down_coordinates = [0, -1]

variations = [left_coordinates, right_coordinates, up_coordinates, down_coordinates]

class Service:

    def __init__(self, drone, environment, dmap):
        self.__drone = drone
        self.__environment = environment
        self.__dmap = dmap

        self.stack = []
        self.stack.append((self.__drone.getX(), self.__drone.getY()))  # the stack used by the DFS in order to push/pop the pairs of position
        # that will be visited (with its neighbors)

        self.knownFields = []  # the fields that are already discovered by the drone
        self.knownFields.append((self.__drone.getX(), self.__drone.getY()))

    def getDrone(self):
        return self.__drone

    def getEnvironment(self):
        return self.__environment

    def getDMap(self):
        return self.__dmap

    def move(self):

        try:
            pressed_keys = pygame.key.get_pressed()
            if self.__drone.getX() > 0:
                if pressed_keys[K_UP] and self.getDMap().getSurface()[self.__drone.getX() - 1][self.__drone.getY()] == 0:
                    self.__drone.setX(self.__drone.getX()- 1)

            if self.__drone.getX() < 19:
                if pressed_keys[K_DOWN] and self.getDMap().getSurface()[self.__drone.getX()  + 1][self.__drone.getY()] == 0:
                    self.__drone.setX(self.__drone.getX() + 1)

            if self.__drone.getY() > 0:
                if pressed_keys[K_LEFT] and self.getDMap().getSurface()[self.__drone.getX()][self.__drone.getY()  - 1] == 0:
                    self.__drone.setY(self.__drone.getY() - 1)
                if pressed_keys[K_RIGHT] and self.getDMap().getSurface()[self.__drone.getX()][self.__drone.getY() + 1] == 0:
                    self.__drone.setY(self.__drone.getY() + 1)
        except Exception as e:
            print("You have reached the edge of the board")

    def moveDFS(self):

        for variation in variations:
            nextX = self.__drone.getX() + variation[0]
            nextY = self.__drone.getY() + variation[1]
            if self.__drone.validPosition(nextX, nextY) and self.getDMap().getValue(nextX, nextY) == 0 and not \
                    self.knownFields.__contains__((nextX, nextY)):
                self.stack.insert(0, (self.__drone.getX(), self.__drone.getY()))  # pushing on the stack the adjacent fields
                self.knownFields.append(
                    (nextX, nextY))  # keeping track of the fields already known by the drone
                self.__drone.setX(nextX)
                self.__drone.setY(nextY)
                return True

        if len(self.stack) == 0:  # the case in which there is no field in the stack (end)
            self.__drone.setX(None)
            self.__drone.setY(None)
            #time.sleep(5)
            return False

        x, y = self.stack.pop(0)  # updating the top of the stack
        self.__drone.setX(x)
        self.__drone.setY(y)

        return True

        # rewrite this function in such a way that you perform an automatic
        # mapping with DFS

    def readUDMSensors(self, x, y):
        readings = [0, 0, 0, 0]

        # if type(x) != int or type(y) != int:
        #     raise Exception("The drone has finished its duty")


        # UP
        xf = x - 1
        while (xf >= 0) and (self.__environment.getSurface()[xf][y] == 0):
            xf = xf - 1
            readings[UP] = readings[UP] + 1
        # DOWN
        xf = x + 1
        while (xf < self.__environment.getN()) and (self.__environment.getSurface()[xf][y] == 0):
            xf = xf + 1
            readings[DOWN] = readings[DOWN] + 1
        # LEFT
        yf = y + 1
        while (yf < self.__environment.getM()) and (self.__environment.getSurface()[x][yf] == 0):
            yf = yf + 1
            readings[LEFT] = readings[LEFT] + 1
        # RIGHT
        yf = y - 1
        while (yf >= 0) and (self.__environment.getSurface()[x][yf] == 0):
            yf = yf - 1
            readings[RIGHT] = readings[RIGHT] + 1

        return readings

    def markDetectedWalls(self, x, y):
        #   To DO
        # mark on this map the walls that you detect
        walls = self.readUDMSensors(x, y)
        i = x - 1
        if walls[UP] > 0:
            while (i >= 0) and (i >= x - walls[UP]):
                self.__dmap.getSurface()[i][y] = 0
                i = i - 1
        if i >= 0:
            self.__dmap.getSurface()[i][y] = 1

        i = x + 1
        if walls[DOWN] > 0:
            while (i < self.__dmap.getN()) and (i <= x + walls[DOWN]):
                self.__dmap.getSurface()[i][y] = 0
                i = i + 1
        if i < self.__dmap.getN():
            self.__dmap.getSurface()[i][y] = 1

        j = y + 1
        if walls[LEFT] > 0:
            while (j < self.__dmap.getM()) and (j <= y + walls[LEFT]):
                self.__dmap.getSurface()[x][j] = 0
                j = j + 1
        if j < self.__dmap.getM():
            self.__dmap.getSurface()[x][j] = 1

        j = y - 1
        if walls[RIGHT] > 0:
            while (j >= 0) and (j >= y - walls[RIGHT]):
                self.__dmap.getSurface()[x][j] = 0
                j = j - 1
        if j >= 0:
            self.__dmap.getSurface()[x][j] = 1

