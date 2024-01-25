from unittest import  TestCase, skip, main as runtest

class Heap:
    
    def __init__(self):
        self.array = list()
        self.last_index = len(self.array)

    def add(self, value):
        self.array.append(value)
        
        current = len(self.array) - 1
        parent = (current-1) // 2
        
        while parent >= 0 and (self.array[parent] < self.array[current]):
            temp = self.array[parent]
            self.array[parent] = self.array[current]
            self.array[current] = temp
            current = parent
            parent = (current-1) // 2

        return self.array
        
    def remove(self):
        ...



class HeapTest(TestCase):
    
    def setUp(self):
        self.heap = Heap()
        return super().setUp()
    
    def test_add_values(self):
        inputs_expected = [
            (46, [46]),
            (35, [46,35]),
            (9,  [46,35,9]),
            (28, [46,35,9,28]),
            (61, [61,46,9,28,35]),
            (8,  [61,46,9,28,35,8]),
            (38, [61,46,38,28,35,8,9]),
            (40, [61,46,38,40,35,8,9,28]),
        ]
        for input, expected in inputs_expected:
            output = self.heap.add(input)
            
            self.assertEqual(output, expected, f"😭 {input}")

if __name__=="__main__":
    runtest()