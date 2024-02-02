from unittest import TestCase, skip, main as runtest
from random import randint
from math import sqrt


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, point):
        return sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)

    def __str__(self):
        return f"({self.x},{self.y})"


class QTree:
    def __init__(
        self, limit=10, min_width=0, max_width=200, min_height=0, max_height=200
    ):
        self.points = []
        self.max_width = max_width
        self.min_width = min_width

        self.max_height = max_height
        self.min_height = min_height

        self.topleft = None
        self.topright = None
        self.downleft = None
        self.downright = None

        self.limit = limit
        self.is_leaf = True

    def inside_limit(self, point):
        return (
            self.min_width <= point.x < self.max_width
            and self.min_height <= point.y < self.max_height
        )

    def subdivide(self):
        limit = self.limit
        top_min, top_max = (
            self.min_height,
            self.min_width + (self.max_width - self.min_width) // 2,
        )

        down_min, down_max = (
            self.min_width + (self.max_width - self.min_width) // 2,
            self.max_width,
        )

        left_min, left_max = (
            self.min_height,
            self.min_height + (self.max_height - self.min_height) // 2,
        )
        right_min, right_max = (
            self.min_height + (self.max_height - self.min_height) // 2,
            self.max_height,
        )

        self.topleft = QTree(limit, top_min, top_max, left_min, left_max)
        self.topright = QTree(limit, top_min, top_max, right_min, right_max)
        self.downleft = QTree(limit, down_min, down_max, left_min, left_max)
        self.downright = QTree(limit, down_min, down_max, right_min, right_max)

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
        if not self.inside_limit(point):
            return []

        if self.is_leaf:
            print(
                f"\n{point} {len(self.points)} x: {self.min_width}, {self.max_width} y: {self.min_height},{self.max_height}"
            )
            return self.points
        else:
            acc = []
            acc += self.topleft.get_near_points(point, radius)
            acc += self.topright.get_near_points(point, radius)
            acc += self.downleft.get_near_points(point, radius)
            acc += self.downright.get_near_points(point, radius)
            return acc


class TestQTree(TestCase):
    def setUp(self) -> None:
        self.qTree = QTree(limit=10)
        return super().setUp()

    def insert_rando_nmumber(self):
        for _ in range(0, 10000):
            p = Point(randint(0, 199), randint(0, 199))
            self.qTree.insert(p)

    @skip
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

    @skip
    def test_Insert_on_quad(self):
        inputs = [Point(50, 50), Point(50, 150), Point(150, 50), Point(150, 150)]
        for point in inputs:
            self.assertTrue(self.qTree.insert(point))

        self.assertEqual(4, len(self.qTree.points))

    @skip
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
        self.assertEqual(5, len(self.qTree.topleft.points))
        self.assertEqual(1, len(self.qTree.topright.points))
        self.assertEqual(1, len(self.qTree.downleft.points))
        self.assertEqual(1, len(self.qTree.downright.points))

    @skip
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
        self.assertEqual(0, len(self.qTree.topleft.points))
        self.assertEqual(1, len(self.qTree.topright.points))
        self.assertEqual(1, len(self.qTree.downleft.points))
        self.assertEqual(1, len(self.qTree.downright.points))

    def test_getting_near_points(self):
        self.insert_rando_nmumber()
        radius = 3
        point_target = Point(95, 65)
        points = self.qTree.get_near_points(point_target, radius)
        for i, point in enumerate(points):
            distance = point.distance(point_target)
            print("\n", i, distance, point)
            # self.assertLess(distance, radius)


if __name__ == "__main__":
    runtest()
