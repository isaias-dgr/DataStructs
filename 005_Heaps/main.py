from unittest import  TestCase, skip, main as runtest

class Heap:
    ## 😂 Will be a better example if the array struct been static you can try with rust and go
    def __init__(self):
        self.array = list()
        self.last_index = -1

    def add(self, value):
        self.array.append(value)
        
        self.last_index += 1 
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
        if self.last_index == -1:
            return None
        
        result =  self.array[0]
        self.array[0] = self.array[self.last_index]
        self.array[self.last_index] = None
        self.last_index -= 1

        i = 0
        while i <= self.last_index:
            swap = i
            if (2*i)+1 <=  self.last_index and (self.array[swap] < self.array[(2*i)+1]):
                swap = (2*i)+1

            if (2*i)+2 <=  self.last_index and (self.array[swap] < self.array[(2*i)+2]):
                swap = (2*i)+2

            if i != swap:
                temp = self.array[i]
                self.array[i] = self.array[swap]
                self.array[swap] = temp
                i = swap
            else: 
                break

        return result

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

    def test_remove_values(self):
        inputs_expected = [46,35,9,28,61,8,38,40]
        for input in inputs_expected:
            output = self.heap.add(input)
        
        outputs_expected = [61, 46, 40, 38, 35, 28, 9, 8]
        # this is more intersting with not arrays dinamics
        for expected in outputs_expected:
            output = self.heap.remove()
            self.assertEqual(output, expected, f"😭 output: {output} expected: {expected}")

        
if __name__=="__main__":
    runtest()