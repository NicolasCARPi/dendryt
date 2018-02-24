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
        #print("cell pos: ", self.cellPos)
        #print("Direction:", direction)

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

            #print("New coord: ", newCoord)

            # check if the target is there
            if self.canvas[tuple(newCoord)] == 1:
                raise Exception

            # place the cell on the canvas
            # can raise IndexError
            self.setPos(newCoord, 2)

            # update the internal cell position
            #print("update cellpos")
            self.cellPos = newCoord

        except IndexError:
            #print("Loop n°{}: Not moving cell out of canvas.".format(self.loop))
            pass


    def initialize(self):
        self.moves = 0
        # CANVAS
        self.canvas = np.zeros((self.canvasSize, self.canvasSize), dtype=int)
        self.targetPos = self.getRandomPos()
        self.setPos(self.targetPos, 1)
        self.setInitialCellPos()

    def launchSearch(self):
        for x in range(0, self.maxMoves):
            try:
                self.moveCell()
                self.moves += 1
            except Exception:
                #print("Target found in {} loops.".format(self.moves))
                self.results.append(self.moves)
                break
        self.initialize()

        #print("Target not found :(")
        #self.results.append(self.maxLoops)

    # start script
    def __init__(self):
        # config
        self.canvasSize = 100
        self.maxMoves = 10000
        self.maxLoops = 100
        # end config

        self.results = []

        self.initialize()

        for x in range(0, self.maxLoops):
            self.launchSearch()

        #print("Cell pos:", self.cellPos)
        # now start the search

        meanMoves = int(np.mean(self.results))
        print("Cell took an average of {} moves to find target in a {}×{} canvas. Tested {} times.".format(meanMoves, self.canvasSize, self.canvasSize, self.maxLoops))

app = Dendryt()
