# import the pygame module, so you can use it
import pickle
import pygame
import time

from pygame.locals import *
from random import random, randint
import numpy as np

# Creating some colors
from Controller.Service import Service
from Model.DMap import DMap
from Model.Drone import Drone
from Model.Environment import Environment

from easygui import *

BLUE = (0, 0, 255)
GRAYBLUE = (50, 120, 120)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

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


class UI:

    def __init__(self, service):
        self.__service = service

    @staticmethod
    def buttons():

        button_list = []
        button1 = "Drone moves using keys"
        button2 = "Drone moves by itself"

        button_list.append(button1)
        button_list.append(button2)
        title = "Drone"
        # window title
        text = "        \n\n                       Welcome to our drone exploration! \n \n" \
               "              Choose the way in which you want the drone to move!\n\n" \
               "            (The drone moves by itself using a Depth First Search) "

        output = buttonbox(text, title, button_list)
        if output == "Drone moves using keys":
            return 1
        return 2

    def mainUI(self, option):

        self.__service.getEnvironment().loadEnvironment(
            "../test2.map")
        pygame.init()
        # load and set the logo
        logo = pygame.image.load(
            "..//logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("drone exploration")

        if not self.__service.getEnvironment().isCorrectlyPlaced(self.__service.getDrone().getX(),
                                                                 self.__service.getDrone().getY()):
            return False

            # create a surface on screen that has the size of 800 x 480
        screen = pygame.display.set_mode((800, 400))
        screen.fill(WHITE)

        screen.blit(self.__service.getEnvironment().image(), (0, 0))

        # define a variable to control the main loop
        running = True

        # main loop
        while running:

            if (option == 1):
                # event handling, gets all event from the event queue
                for event in pygame.event.get():
                    # only do something if the event is of type QUIT
                    if event.type == pygame.QUIT:
                        # change the value to False, to exit the main loop
                        running = False
                    self.__service.move()
            else:

                self.__service.moveDFS()
                #time.sleep(0.050)

            x = self.__service.getDrone().getX()
            y = self.__service.getDrone().getY()

            self.__service.markDetectedWalls(x, y)
            screen.blit(
                self.__service.getDMap().image(self.__service.getDrone().getX(), self.__service.getDrone().getY()),
                (400, 0))
            pygame.display.flip()

        pygame.quit()

        return True


if __name__ == "__main__":

    # we position the drone somewhere in the area
    x = randint(0, 19)
    y = randint(0, 19)

    drone = Drone(x, y)
    environment = Environment()
    dmap = DMap()

    service = Service(drone, environment, dmap)
    ui = UI(service)

    try:
        option = ui.buttons()
        ui.mainUI(option)
    except Exception as e:
        print(str(e))
        print("We have to replace the drone")
        time.sleep(2)
