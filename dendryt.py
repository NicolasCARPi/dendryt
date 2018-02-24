#!/usr/bin/env python
import numpy as np
from random import randint
from random import choice

class Dendryt():
    # get a random position on the canvas
    def getRandomPos(self):
        return [randint(0, self.canvasSize - 1), randint(0, self.canvasSize -1)]

    # place the target on canvas
    def setPos(self, pos, value):
        self.canvas[tuple(pos)] = value

    def setInitialCellPos(self):
        cellPos = self.getRandomPos()
        # if we are on target get a new position, otherwise it's too easy :p
        while True:
            if cellPos != self.targetPos:
                self.setPos(cellPos, 2)
                self.cellPos = cellPos
                break
            else:
                cellPos = self.getRandomPos()


    # cell can get N S E or W
    def getDirection(self):
        directions = ['N', 'E', 'S', 'W']
        return choice(directions)

    # cell position
    def moveCell(self):

        direction = self.getDirection()
        print("cell pos: ", self.cellPos)
        print("Direction:", direction)

        try:
            if direction == 'N':
                newPos = self.cellPos[0] - 1
                newCoord = [self.cellPos[0] - 1, self.cellPos[1]]
            elif direction == 'E':
                newPos = self.cellPos[1] + 1
                newCoord = [self.cellPos[0], self.cellPos[1] + 1]
            elif direction == 'S':
                newPos = self.cellPos[0] + 1
                newCoord = [self.cellPos[0] + 1, self.cellPos[1]]
            elif direction == 'W':
                newPos = self.cellPos[1] - 1
                newCoord = [self.cellPos[0], self.cellPos[1] - 1]

            print("New coord: ", newCoord)

            # check if the target is there
            if self.canvas[tuple(newCoord)] == 1:
                print("Target found in {} loops.".format(self.loops))
                raise SystemExit

            # place the cell on the canvas
            if direction == 'N' or direction == 'S':
                self.setPos([newPos, self.cellPos[1]], 2)
                #self.cellPos[0] = newPos
            else:
                #self.cellPos[1] = newPos
                self.setPos([self.cellPos[0], newPos], 2)
            self.cellPos = newCoord

        except IndexError:
            print("Cell is not moving out of canvas.")


    # start script
    def __init__(self):
        # config
        self.canvasSize = 100
        maxLoops = 1000000
        # end config

        self.loops = 0

        # CANVAS
        self.canvas = np.zeros((self.canvasSize, self.canvasSize), dtype=int)
        self.targetPos = self.getRandomPos()
        self.setPos(self.targetPos, 1)

        self.setInitialCellPos()
        print(self.canvas)

        print("Cell pos:", self.cellPos)
        # now start the search
        for x in range(0, maxLoops):
            self.moveCell()
            self.loops += 1
            print(self.canvas)
        print("Target not found :(")

app = Dendryt()
