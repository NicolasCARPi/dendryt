#!/usr/bin/env python
import os
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from random import randint
from random import choice

class Dendryt():
    def getRandomPos(self):
        """
            Get a random position on the canvas
        """
        return [randint(0, self.canvasSize - 1), randint(0, self.canvasSize -1)]

    def setPos(self, pos, value):
        """
            Change a value on the canvas
        """
        self.canvas[tuple(pos)] = value

    def setInitialCellPos(self):
        """
            Set the starting position of the cell
        """
        cellPos = self.getRandomPos()
        # if we are on target get a new position, otherwise it's too easy :p
        while True:
            if cellPos != self.targetPos:
                self.cellPos = self.startPos = cellPos

                # make the cell visible on canvas
                self.setPos(self.cellPos, 255)
                break
            else:
                # get a new random position and try again
                cellPos = self.getRandomPos()

        #with open("results" + os.sep + "loop-" + str(self.currentLoop) + ".txt", "w") as log:
        #    log.write("Starting at cell position:" + str(self.cellPos))
        #    log.write("Target is at position:" + str(self.targetPos))
        #log.close()


    def getDirection(self):
        """
            Select where to go. Returns 'N', 'S', 'E' or 'W'.
        """
        # are we still persistant?
        if (randint(0, 100) > self.persistanceIndex):
            # invert persistance mode
            self.persistance = not self.persistance

        # if we are in bullet mode continue in same direction
        if (self.persistance):
            return self.previousDir

        directions = ['N', 'E', 'S', 'W']
        return choice(directions)

    def moveCell(self):
        """
            Move the cell of one unit in a direction
        """

        # save the previous direction
        direction = self.previousDir = self.getDirection()

        try:
            if direction == 'N':
                newPos = self.cellPos[0] - 1
                if newPos < 0:
                    newPos = 0
                if newPos > self.canvasSize - 1:
                    newPos = self.canvasSize - 1
                newCoord = [newPos, self.cellPos[1]]
            elif direction == 'E':
                newPos = self.cellPos[1] + 1
                if newPos < 0:
                    newPos = 0
                if newPos > self.canvasSize - 1:
                    newPos = self.canvasSize - 1
                newCoord = [self.cellPos[0], newPos]
            elif direction == 'S':
                newPos = self.cellPos[0] + 1
                if newPos < 0:
                    newPos = 0
                if newPos > self.canvasSize - 1:
                    newPos = self.canvasSize - 1
                newCoord = [newPos, self.cellPos[1]]
            elif direction == 'W':
                newPos = self.cellPos[1] - 1
                if newPos < 0:
                    newPos = 0
                if newPos > self.canvasSize - 1:
                    newPos = self.canvasSize - 1
                newCoord = [self.cellPos[0], newPos]
            #with open("results" + os.sep + "loop-" + str(self.currentLoop) + ".txt", "a") as log:
            #    log.write("Moving cell", direction)
            #    log.close()

            #print("New coord:", newCoord)
            # check if the target is there
            if newCoord == self.targetPos:
                raise Exception

            # place the cell on the canvas
            # can raise IndexError
            self.setPos(newCoord, 128)

            # update the internal cell position
            self.cellPos = newCoord

        except IndexError:
            print("Loop n°{}: Not moving cell out of canvas.".format(self.loop))
            print("Previous dir: ", self.previousDir)
            # go back where we came from
            self.persistance = True
            self.previousDir = self.getInverseDirection(direction)
            print("Previous dir after inversion: ", self.previousDir)
            pass

    def getInverseDirection(self, direction):
        """
            Go back from where you come
        """
        if direction == 'N':
            return 'S'
        elif direction == 'E':
            return 'W'
        elif direction == 'S':
            return 'N'
        elif direction == 'W':
            return 'E'

    def initialize(self):
        """
            Initialize canvas to zeros. Set the target and initial cell positions.
        """
        self.persistance = False
        self.previousDir = 'N'
        self.canvas = np.zeros((self.canvasSize, self.canvasSize), dtype=int)
        # where the target is
        self.targetPos = self.getRandomPos()
        self.setPos(self.targetPos, 255)
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
                #print("Target found in {} moves.".format(move))
                self.results.append(move)

                # recolor the start position
                self.canvas[tuple(self.startPos)] = 200

                # draw image
                fig = plt.figure()
                plt.imshow(self.canvas, cmap='Greens')
                plt.title("Target found in {} moves. Start {}. Target {}".format(move, self.startPos, self.targetPos))
                #plt.show()
                fig.savefig("results" + os.sep + "loop-" + str(self.currentLoop) + ".png", dpi=200)
                plt.close()
                break

    def __init__(self):
        """
            Start the script
        """
        # CONFIG
        self.canvasSize = 500
        self.maxLoops = 20
        self.maxMoves = 10000000
        # between 1 and 100
        self.persistanceIndex = 69
        # END CONFIG

        # where we store the number of moves required to find target
        self.results = []
        self.currentLoop = 0

        self.initialize()

        # now do the loops
        for loop in range(0, self.maxLoops):
            self.currentLoop = loop
            self.launchSearch()
            self.initialize()

        meanMoves = int(np.mean(self.results))
        stdDev = int(np.std(self.results))
        print("Cell took an average of {} moves to find target in a {}×{} canvas. Tested {} times. Standard deviation of {}".format(meanMoves, self.canvasSize, self.canvasSize, self.maxLoops, stdDev))

app = Dendryt()
