#!/usr/bin/env python
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
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
                #self.setPos(cellPos, 2)
                self.cellPos = cellPos
                #self.startingPos = cellPos
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

        try:
            if direction == 'N':
                newPos = self.cellPos[0] - 1
                if newPos < 0:
                    newPos = 0
                newCoord = [newPos, self.cellPos[1]]
            elif direction == 'E':
                newPos = self.cellPos[1] + 1
                if newPos < 0:
                    newPos = 0
                newCoord = [self.cellPos[0], newPos]
            elif direction == 'S':
                newPos = self.cellPos[0] + 1
                if newPos < 0:
                    newPos = 0
                newCoord = [newPos, self.cellPos[1]]
            elif direction == 'W':
                newPos = self.cellPos[1] - 1
                if newPos < 0:
                    newPos = 0
                newCoord = [self.cellPos[0], newPos]

            # check if the target is there
            if newCoord == self.targetPos:
                raise Exception

            # place the cell on the canvas
            # can raise IndexError
            self.setPos(newCoord, 2)

            # update the internal cell position
            self.cellPos = newCoord

        except IndexError:
            #print("Loop n°{}: Not moving cell out of canvas.".format(self.loop))
            pass


    def initialize(self):
        """
            Initialize canvas to zeros. Set the target and initial cell positions.
        """
        self.canvas = np.zeros((self.canvasSize, self.canvasSize), dtype=int)
        # where the target is
        self.targetPos = self.getRandomPos()
        # create the cell in a random position
        self.setInitialCellPos()

    def launchSearch(self):
        """
            Move the cell around to try and find the target.
        """
        for move in range(0, self.maxMoves):
            try:
                self.moveCell()
            except Exception:
                #print("Target found in {} loops.".format(move))
                self.results.append(move)
                break

    def __init__(self):
        """
            Start the script
        """
        # CONFIG
        self.canvasSize = 10
        self.maxLoops = 10000
        self.maxMoves = 1000000
        # END CONFIG

        # where we store the number of moves required to find target
        self.results = []

        self.initialize()

        # now do the loops
        for x in range(0, self.maxLoops):
            self.launchSearch()
            self.initialize()

        meanMoves = int(np.mean(self.results))
        stdDev = int(np.std(self.results))
        print("Cell took an average of {} moves to find target in a {}×{} canvas. Tested {} times. Standard deviation of {}".format(meanMoves, self.canvasSize, self.canvasSize, self.maxLoops, stdDev))

app = Dendryt()
