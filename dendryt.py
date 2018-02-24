#!/usr/bin/env python
import numpy as np
from random import randint

class Dendryt():
    # get a random position on the canvas
    def getRandomPos(self):
        return (randint(0, self.canvasSize - 1), randint(0, self.canvasSize -1))

    # place the target on canvas
    def setPos(self, pos, value):
        self.canvas[pos[0], pos[1]] = value

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

    # cell position
    def moveCell(self):
        newPosX = self.cellPos[0] + 1
        if newPosX > self.canvasSize - 1:
            newPosX = self.cellPos[0] - randint(0, self.canvasSize - 1)
        newPosY = self.cellPos[1] + 1
        if newPosY > self.canvasSize - 1:
            newPosY = self.cellPos[1] - randint(0, self.canvasSize - 1)

        self.cellPos = (newPosX, newPosY)

        if self.canvas[self.cellPos] == 1:
            print("Target found in {} loops.".format(self.loops))
            raise SystemExit

        self.setPos(self.cellPos, 2)

    # start script
    def __init__(self):
        # config
        self.canvasSize = 100
        maxLoops = 10000000
        # end config

        self.loops = 0

        # CANVAS
        self.canvas = np.zeros((self.canvasSize, self.canvasSize), dtype=int)
        self.targetPos = self.getRandomPos()
        self.setPos(self.targetPos, 1)

        self.setInitialCellPos()
        for x in range(0, maxLoops):
            self.moveCell()
            self.loops += 1
        print("Target not found :(")

app = Dendryt()
