#!/usr/bin/env python
import os
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from random import randint
from random import choice

class Dendryt():
    # CONFIG
    CANVAS_SIZE = 100
    MAX_LOOPS = 20
    MAX_MOVES = 20000
    # BETWEEN 1 AND 99
    PERSISTANCE_INDEX = 89
    SHOW_LOOPS = True
    # END CONFIG

    def getRandomPos(self):
        """
            Get a random position on the canvas
        """
        return [randint(0, self.CANVAS_SIZE - 1), randint(0, self.CANVAS_SIZE -1)]

    def setPos(self, pos, value):
        """
            Change a value on the canvas
        """
        self.canvas[tuple(pos)] = value

    def setInitialCellPos(self):
        """
            Set the starting position of the cell
        """
        self.cellPos = self.startPos = self.getRandomPos()
        self.setPos(self.cellPos, 255)

    def getDirection(self):
        """
            Select where to go. Returns 'N', 'S', 'E' or 'W'.
        """
        # are we still persistant?
        if (randint(0, 100) > self.PERSISTANCE_INDEX):
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

        # get a new direction and save it
        direction = self.previousDir = self.getDirection()

        try:
            if direction == 'N':
                newPos = self.cellPos[0] - 1
                if newPos < 0:
                    newPos = 0
                if newPos > self.CANVAS_SIZE - 1:
                    newPos = self.CANVAS_SIZE - 1
                newCoord = [newPos, self.cellPos[1]]
            elif direction == 'E':
                newPos = self.cellPos[1] + 1
                if newPos < 0:
                    newPos = 0
                if newPos > self.CANVAS_SIZE - 1:
                    newPos = self.CANVAS_SIZE - 1
                newCoord = [self.cellPos[0], newPos]
            elif direction == 'S':
                newPos = self.cellPos[0] + 1
                if newPos < 0:
                    newPos = 0
                if newPos > self.CANVAS_SIZE - 1:
                    newPos = self.CANVAS_SIZE - 1
                newCoord = [newPos, self.cellPos[1]]
            elif direction == 'W':
                newPos = self.cellPos[1] - 1
                if newPos < 0:
                    newPos = 0
                if newPos > self.CANVAS_SIZE - 1:
                    newPos = self.CANVAS_SIZE - 1
                newCoord = [self.cellPos[0], newPos]
            #with open("results" + os.sep + "loop-" + str(self.currentLoop) + ".txt", "a") as log:
            #    log.write("Moving cell", direction)
            #    log.close()

            #print("New coord:", newCoord)
            # check if the target is there
            #if newCoord == self.targetPos:
            #    raise Exception

            # place the cell on the canvas
            # can raise IndexError
            self.setPos(newCoord, 255)

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
        self.canvas = np.zeros((self.CANVAS_SIZE, self.CANVAS_SIZE), dtype=int)
        # where the target is
        #self.targetPos = self.getRandomPos()
        #self.setPos(self.targetPos, 255)
        # create the cell in a random position
        self.setInitialCellPos()

    def launchSearch(self):
        """
            Move the cell around to try to cover the most ground
        """
        for move in range(0, self.MAX_MOVES):
            self.moveCell()

        # the score is the mean value of the image
        score = np.mean(self.canvas)

        if self.SHOW_LOOPS:
            # draw image
            fig = plt.figure()
            plt.imshow(self.canvas, cmap='Greens')
            plt.title("Score: " + str(score))
            loopDir = "results" + os.sep + 'persistance-' + str(self.PERSISTANCE_INDEX)
            if not os.path.exists(loopDir):
                os.makedirs(loopDir)
            fig.savefig(loopDir + os.sep + "loop-" + str(self.currentLoop) + ".png", dpi=200)
            plt.close()

        return score

    def __init__(self):
        """
            Start the script
        """
        # where we store the number of moves required to find target
        self.results = []
        self.finalResults = []
        self.currentLoop = 0

        self.initialize()

        for assay in range(1, 99):
            scores = []
            self.PERSISTANCE_INDEX = assay
            print("Now testing with persistance index of {}.".format(assay))
            # now do the loops
            for loop in range(0, self.MAX_LOOPS):
                self.currentLoop = loop
                scores.append(self.launchSearch())
                self.initialize()

            print("Mean score:", np.mean(scores))
            self.finalResults.append(np.mean(scores))

        fig = plt.figure()
        plt.plot(self.finalResults)
        plt.title("Mean surface covered in {} moves as function of persistance index.".format(self.MAX_MOVES))
        plt.xlabel("Persistance index")
        plt.ylabel("Mean surface covered (" + str(self.MAX_LOOPS) + " iterations)")
        fig.savefig("results" + os.sep + "final-results.png", dpi=200)
        plt.close()

app = Dendryt()
