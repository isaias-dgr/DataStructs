from unittest import TestCase, skip, main as runtest
from math import sqrt, floor
import random


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, point):
        return sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)

    def __str__(self):
        return f"({self.x}, {self.y})"


class Grid:
    def __init__(self, size_grid, max_size_bin=10):
        self.grid = [[list() for _ in range(size_grid)] for _ in range(size_grid)]
        self.__max_size_bin = max_size_bin
        self.__size_bin = max_size_bin / size_grid

    def add(self, point):
        column = floor((point.x) / self.__size_bin)
        row = floor((point.y) / self.__size_bin)
        if not (0 <= column <= self.__max_size_bin) and not (
            0 <= row <= self.__max_size_bin
        ):
            return None

        self.grid[column][row].append(point)

    # code duplicated
    def get_bind(self, col, row, radius=0):
        if radius > 0:
            min_col = 0 if col - radius < 0 else col - radius
            max_col = col + radius + 1
            min_row = 0 if row - radius < 0 else row - radius
            max_row = row + radius + 1
            return [c[min_row:max_row] for c in self.grid[min_col:max_col]]

        return self.grid[col][row]

    def get_bind_data(self, col, row, radius=0):
        output = []
        if radius > 0:
            min_col = 0 if col - radius < 0 else col - radius
            max_col = col + radius + 1
            min_row = 0 if row - radius < 0 else row - radius
            max_row = row + radius + 1
            for c in self.grid[min_col:max_col]:
                for r in c[min_row:max_row]:
                    output += r
        else:
            output += self.grid[col][row]

        return output

    def get_nearby_neighborhood(self, point_target, radius=0):
        column = floor((point_target.x) / self.__size_bin)
        row = floor((point_target.y) / self.__size_bin)

        if not (0 <= column <= self.__max_size_bin) and not (
            0 <= row <= self.__max_size_bin
        ):
            return None

        neighborhood = []
        for point in self.get_bind_data(column, row, radius):
            distance = point_target.distance(point)
            neighborhood.append((distance, point))

        neighborhood.sort(key=lambda x: x[0])
        return neighborhood


class GridTest(TestCase):
    def setUp(self) -> None:
        self.grid = Grid(3, 10)  # grid nxn values 0 to 10
        return super().setUp()

    def test_add(self):
        points = [
            ((0, 0), Point(1, 1)),
            ((0, 1), Point(1, 4)),
            ((0, 2), Point(1, 7)),
            ((1, 0), Point(4, 1)),
            ((1, 1), Point(4, 4)),
            ((1, 2), Point(4, 7)),
            ((2, 0), Point(7, 1)),
            ((2, 1), Point(7, 4)),
            ((2, 2), Point(7, 7)),
        ]
        for (x, y), point in points:
            self.grid.add(point)
            bind = self.grid.get_bind(x, y)
            self.assertEqual([point], bind)

        points = [Point(1.423, 1.242), Point(1, 2.423), Point(1, 0.342)]
        for point in points:
            self.grid.add(point)

        bind = self.grid.get_bind(0, 0)
        self.assertEqual(4, len(bind))

    def test_nearby_neighborhood(self):
        self.grid = Grid(3, 10)
        points = [
            Point(1, 1),
            Point(1, 4),
            Point(1, 7),
            Point(4, 1),
            Point(4, 4),
            Point(4, 7),
            Point(7, 1),
            Point(7, 4),
            Point(7, 7),
        ]
        for p in points:
            self.grid.add(p)

        neighborhood = self.grid.get_nearby_neighborhood(Point(0.342, 0.99), 1)
        distance, point = neighborhood[0]
        self.assertEqual(0.6580759834547982, distance)
        self.assertEqual(points[0], point)
        distance, point = neighborhood[-1]
        self.assertEqual(4.737200016887613, distance)
        self.assertEqual(points[4], point)


if __name__ == "__main__":
    runtest()
