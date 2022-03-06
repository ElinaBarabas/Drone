
class Drone:

    def __init__(self, x, y):
        self.__x = x
        self.__y = y


        self.stack = []
        self.stack.append((self.__x, self.__y))  # the stack used by the DFS in order to push/pop the pairs of position
        # that will be visited (with its neighbors)

        self.knownFields = []  # the fields that are already discovered by the drone
        self.knownFields.append((self.__x, self.__y))

    def setX(self, newX):
        self.__x = newX

    def setY(self, newY):
        self.__y = newY

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    @staticmethod
    def validPosition(xCoordinate, yCoordinate):
        return 0 <= xCoordinate < 20 and 0 <= yCoordinate < 20



