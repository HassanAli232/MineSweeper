
from PyQt6.QtWidgets import (
    QGridLayout    
)
from cell import Cell
import random
import numpy as np

class SweeperGrid(QGridLayout):

    def __init__(self, rows: int, cols: int, n: int = -1):
        super().__init__()

        self.setSpacing(0)

        self.rows = rows
        self.cols = cols
        self.n = n if n != -1 else self.rows * self.cols // 10

        indices = self._generate_unique_indices(self.rows * self.cols, self.n)
        self.cells = np.empty((self.rows, self.cols), dtype=Cell)
        
        
        for i in range(self.rows):
            for j in range(self.cols):
                cell = Cell(i, j, self)
                self.cells[i, j] = cell
                self.addWidget(cell, i, j)
        

        for i, j in indices:
            self.cells[i, j].setState()

            for x in [i-1, i, i+1]:
                for y in [j-1, j, j+1]:
                    if (x == i and y == j) or x < 0 or x >= self.rows or y < 0 or y >= self.cols:
                        continue
                    self.cells[x, y].incrementMines()
        
        # for i in range(self.rows):
        #     for j in range(self.cols):
        #         self.cells[i, j].show()

    def endGame(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i, j].show()


    def trigger(self, x, y):

        for i in [x-1, x, x+1]:
            for j in [y-1, y, y+1]:
                
                if (x == i and y == j) or i < 0 or i >= self.rows or j < 0 or j >= self.cols:
                    continue
                # print(i, j)
                self.cells[i, j].show() # type: ignore
                
        
    
    def _generate_unique_indices(self, list_size, num_indices):
        if num_indices > list_size:
            raise ValueError("Number of indices cannot be greater than list size.")
        indices = random.sample(range(list_size), num_indices)
        indices = list(map(lambda index: (index//self.cols, index % self.cols), indices))
        return indices
        