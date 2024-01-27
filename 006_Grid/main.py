from unittest import TestCase, skip, main as runtest
from math import sqrt

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, point):
        return sqrt( (self.x - point.x) ** 2 + (self.y - point.y) ** 2) 
    

    def __str__(self):
        return f"({self.x}, {self.y})"


class Grid:

    def __init__(self, columns, rows):
        self.grid = [ [[]] * columns for _ in range(rows)  ]
        self.__size_x = columns
        self.__size_y = rows

    def add(self, point):
        self.column = (point.x) // self.__size_x
        self.row = (point.y) // self.__size_y
        
        if not (0 <= self.column <= self.__size_x) and \
           not (0 <= self.row <= self.__size_y):
            return None
        
        self.grid[self.column][self.row].append(point)

    def get_bind(self, col, row):
        return self.grid[col][row]


class GridTest(TestCase):

    def setUp(self) -> None:
        self.grid = Grid(9, 9)
        return super().setUp()
    
    def test_add(self):
        p = Point(1, 1)
        self.grid.add(p)
        bind = self.grid.get_bind(0, 0)
        self.assertEqual([p], bind)
        
if __name__ == "__main__":
    runtest()
