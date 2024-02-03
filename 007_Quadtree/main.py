import dis
from unittest import TestCase, skip, main as runtest
from random import randint
from math import sqrt

from django.http import QueryDict


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, point):
        return sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)

    def __str__(self):
        return f"({self.x},{self.y})"


class QTree:
    def __init__(self, limit=10, min_x=0, max_x=200, min_y=0, max_y=200):
        self.points = []
        self.max_x = max_x
        self.min_x = min_x

        self.max_y = max_y
        self.min_y = min_y

        self.topleft = None
        self.topright = None
        self.downleft = None
        self.downright = None

        self.limit = limit
        self.is_leaf = True

    def inside_limit(self, point):
        return self.min_x <= point.x < self.max_x and self.min_y <= point.y < self.max_y

    def subdivide(self):
        limit = self.limit
        top_min, top_max = (
            self.min_y,
            self.min_x + (self.max_x - self.min_x) // 2,
        )

        down_min, down_max = (
            self.min_x + (self.max_x - self.min_x) // 2,
            self.max_x,
        )

        left_min, left_max = (
            self.min_y,
            self.min_y + (self.max_y - self.min_y) // 2,
        )
        right_min, right_max = (
            self.min_y + (self.max_y - self.min_y) // 2,
            self.max_y,
        )

        self.topleft = QTree(limit, top_min, top_max, right_min, right_max)
        self.topright = QTree(limit, down_min, down_max, right_min, right_max)
        self.downleft = QTree(limit, top_min, top_max, left_min, left_max)
        self.downright = QTree(limit, down_min, down_max, left_min, left_max)

        self.is_leaf = False

        for point in self.points:
            self.__insert_in_Childs(point)

        self.points = []

    def __insert_in_Childs(self, point):
        if self.topleft.insert(point):
            return True
        elif self.topright.insert(point):
            return True
        elif self.downleft.insert(point):
            return True
        elif self.downright.insert(point):
            return True

    def insert(self, point):
        if not self.inside_limit(point):
            return False

        if self.is_leaf:
            if len(self.points) < self.limit:
                self.points.append(point)
                return True
            self.subdivide()

        self.__insert_in_Childs(point)

    def get_near_points(self, point, radius=1):
        points = self.__get_near_points(point, radius)
        acc = []

        for p in points:
            dist = p.distance(point)
            if dist <= radius:
                acc.append((dist, p))
        acc.sort(key=lambda x: x[0])
        return acc

    def get_min_dist(self, point, radius):
        dist_min_x = min(abs(point.x - self.max_x), abs(point.x - self.min_x))
        dist_min_y = min(abs(point.y - self.max_y), abs(point.y - self.min_y))
        return dist_min_x < radius and dist_min_y < radius

    def __get_near_points(self, point, radius=1):
        acc = []
        near_quad = self.get_min_dist(point, radius)
        if not self.inside_limit(point) and not near_quad:
            return []

        if self.is_leaf and near_quad:
            return self.points

        acc += self.topleft.__get_near_points(point, radius)
        acc += self.topright.__get_near_points(point, radius)
        acc += self.downleft.__get_near_points(point, radius)
        acc += self.downright.__get_near_points(point, radius)
        return acc

    def __str__(self):
        if self.is_leaf:
            return f"{self.points}"

        topleft = [str(p) for p in self.topleft.points]
        topright = [str(p) for p in self.topright.points]
        downleft = [str(p) for p in self.downleft.points]
        downright = [str(p) for p in self.downright.points]
        return f"topleft: {topleft}\ntopright: {topright}\ndownleft {downleft}\ndownright {downright}"


class TestQTree(TestCase):
    def setUp(self) -> None:
        self.qTree = QTree(limit=5)
        return super().setUp()

    def insert_rando_nmumber(self):
        for _ in range(0, 1000):
            p = Point(randint(0, 199), randint(0, 199))
            self.qTree.insert(p)

    def test_Insert_fail_out_of_limits(self):
        inputs = [
            Point(-1, 0),
            Point(0, -1),
            Point(-1, -1),
            Point(201, 0),
            Point(0, 201),
            Point(201, 201),
        ]
        for point in inputs:
            self.assertFalse(self.qTree.insert(point))

    def test_Insert_on_quad(self):
        inputs = [Point(50, 50), Point(50, 150), Point(150, 50), Point(150, 150)]
        for point in inputs:
            self.assertTrue(self.qTree.insert(point))

        self.assertEqual(4, len(self.qTree.points))

    def test_Insert_subdive_and_redistribute(self):
        inputs = [
            Point(50, 50),
            Point(50, 51),
            Point(49, 49),
            Point(50, 49),
            Point(51, 51),
            Point(50, 150),
            Point(150, 50),
            Point(150, 150),
        ]
        for point in inputs:
            self.qTree.insert(point)

        self.assertEqual(0, len(self.qTree.points))
        self.assertEqual(5, len(self.qTree.downleft.points))
        self.assertEqual(1, len(self.qTree.downright.points))
        self.assertEqual(1, len(self.qTree.topleft.points))
        self.assertEqual(1, len(self.qTree.topright.points))

    def test_Insert_subdive_and_redistribute_two_levels(self):
        inputs = [
            Point(50, 50),
            Point(50, 51),
            Point(49, 49),
            Point(50, 49),
            Point(51, 51),
            Point(52, 51),
            Point(50, 150),
            Point(150, 50),
            Point(150, 150),
        ]
        for point in inputs:
            self.qTree.insert(point)

        self.assertEqual(0, len(self.qTree.points))
        self.assertEqual(0, len(self.qTree.downleft.points))
        self.assertEqual(1, len(self.qTree.downright.points))
        self.assertEqual(1, len(self.qTree.topleft.points))
        self.assertEqual(1, len(self.qTree.topright.points))

    def test_getting_near_points(self):
        self.insert_rando_nmumber()
        points = self.qTree.get_near_points(Point(50, 50), 50)

        for distance, p in points:
            self.assertLessEqual(distance, 50)


if __name__ == "__main__":
    runtest()
