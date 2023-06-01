import pyautogui as pg
import numpy as np
import skimage
import time
from PIL import Image


class Game():
    TL = [623, 350]
    BR = [1300, 875]
    SQUAREL = 37.5
    #0,0,1,1,2,3,4,5,6,4
    COLOURLIST = [[226, 192, 158],[214, 184, 152],[172, 171, 158], [139, 160, 137], [141, 165, 109], [199, 121, 87], [181, 130, 152], [180, 167, 55], [101, 168, 130], [157, 131, 120]]

    def __init__(self, sizex, sizey):
        self.gameOver = False
        # medium board is 14x18, 40 mines
        self.state = [[0 for y in range(sizey)] for x in range(sizex)]
        self.opened = [[0 for y in range(sizey)] for x in range(sizex)]
        self.sizex = sizex
        self.sizey = sizey
        self.lastUpdate = time.time()
        self.mines = 40


    def get_colourval(self, pboard):
        board = pboard.copy()

        for i in reversed(range(18)):
            cur = int(i*37.5)
            board = np.delete(board, np.s_[cur-5:cur+3], 1)
        for i in reversed(range(14)):
            cur = int(i * 37.5)
            board = np.delete(board, np.s_[cur-5:cur+3], 0)
        board = np.delete(board, 0, 0)
        board = np.insert(board, 537, 255, 1)
        board = skimage.measure.block_reduce(board, (5, 5, 1), np.min)
        board = skimage.measure.block_reduce(board, (6, 6, 1), np.mean)
        return board

    def closest(self, color):
        colors = np.array(self.COLOURLIST)
        distances = np.sqrt(np.sum((colors - color) ** 2, axis=1))
        index_of_smallest = np.where(distances == np.amin(distances))
        if index_of_smallest[0][0] <=1:
            return 0
        elif index_of_smallest[0][0]<=3:
            return 1
        elif index_of_smallest[0][0]== 9:
            return 4
        return index_of_smallest[0][0]-2

    def test(self):
        board = np.asarray(pg.screenshot(region=(623, 350, 675, 525)))
        colourboard = self.get_colourval(board)
        img = Image.fromarray(colourboard.astype('uint8'), 'RGB')
        img.show()

    def get_board(self):
        board = np.asarray(pg.screenshot(region=(623, 350, 675, 525)))
        colourboard = self.get_colourval(board)
        for y in range(self.sizey):
            for x in range(self.sizex):
                if board[int(y * self.SQUAREL + 20)][int(x * self.SQUAREL + 25)][1] < 200 or board[int(y * self.SQUAREL + 20)][int(x * self.SQUAREL + 25)][2] > 140:
                    self.state[x][y] = self.closest(colourboard[y][x])
                    self.opened[x][y] = 1

    def flag(self, x, y):
        if self.opened[x][y] == 0:
            self.mines += 1
            self.opened[x][y] = 2
        else:
            self.mines -= 1
            self.opened[x][y] = 0
        pg.click(self.TL[0] + int(self.SQUAREL * x) + 20, self.TL[1] + int(self.SQUAREL * y) + 15, button='right')

    def open(self, x, y):
        self.opened[x][y] = 1
        pg.click(self.TL[0] + int(self.SQUAREL * x) + 20, self.TL[1] + int(self.SQUAREL * y) + 15, button='left')
        self.lastUpdate = time.time()