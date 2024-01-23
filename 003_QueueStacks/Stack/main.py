import unittest 

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
    
    def __str__(self):
        return str(self.data)

class Stack:
    def __init__(self):
        self.head = None

    def push(self, value):
        new_node = Node(value)
        if self.head:
            new_node.next = self.head
        self.head = new_node

    def pop(self):
        node = self.head
        if node:
            self.head = node.next
        return node.data if node else None

    def __str__(self):
        stack = "< "
        for node in self:
            stack += str(node) + str(", " if node.next else "")
        return stack + " >"

    def __iter__(self):
        node = self.head
        while node:
            yield node
            node = node.next

# class StackTest(unittest.TestCase):

#     def setUp(self) -> None:
#         self.stack = Stack()
#         return super().setUp()
    
#     def test_empty_stack(self):
#         stack_str = str(self.stack)
#         expected = "<  >"
#         self.assertEqual(stack_str, expected)

#     def test_insert_objects(self):
#         self.stack.push(Node(1))
#         self.stack.push(Node("2"))
#         self.stack.push(Node("hola"))
    
#         stack_str = str(self.stack)
#         expected = "< hola, 2, 1 >"
#         self.assertEqual(stack_str, expected)

#     def test_delete_objects(self):
#         self.stack.push(Node(1))
#         self.stack.push(Node("2"))
#         self.stack.push(Node("hola"))
#         node = self.stack.pop()
#         expected = "hola"
#         self.assertEqual(node.data, expected)

#         self.stack.pop()
#         stack_str = str(self.stack) 
#         expected = "< 1 >"
#         self.assertEqual(stack_str, expected)

#     def test_delete_empty_stack(self):
#         node = self.stack.pop()
#         self.assertIsNone(node)

class Tree():

    def __init__(self, tree, root):
        self.tree = tree
        self.root = root
        self.stack = Stack()
        self.stack.push(self.root)

    def set_new_root_path(self, root):
        self.root = root
        self.stack = Stack()
        self.stack.push(self.root)

    def DFS(self, target):
        node = self.stack.pop()
        explored = [node]
        while node:
            children = self.tree.get(node, [])
            for child in children:
                if child in explored:
                    continue
                if child == target:
                    return True, child
                explored.append(child)
                self.stack.push(child)
            node = self.stack.pop()
        return False, None

    def DFS_path(self, target, root = "a"):
        self.set_new_root_path([root])
        path = self.stack.pop()[::]
        explored = set()
        while path:
            node = path[-1]
            children = self.tree.get(node, [])
            for child in children:
                if child in explored:
                    continue
                new_path = path[::]
                new_path.append(child)
                if child == target:
                    return True, new_path
                explored.add(node)            
                self.stack.push(new_path)
            path = self.stack.pop()            
        return False, None


class DFSTest(unittest.TestCase):

    def setUp(self) -> None:
        tree = {
            "a": ["b", "c", "d"],
            "b": ["e", "f", "g", "h"],
            "c": ["i", "j", "k", "l", "m"],
            "d": ["1"],
            "e": ["n","o"],
            "f": ["p"],
            "g": ["q"],
            "h": ["r"],
            "i": ["s"],
            "j": ["t"],
            "k": ["u"],
            "l": ["v", "x"],
            "m": ["y", "z", "isaias"],
        }
        self.tree = Tree(tree, "a")
        return super().setUp()
    
    def test_search_target_success(self):
        status, value = self.tree.DFS("isaias")
        self.assertTrue(status)
        self.assertEqual(value, "isaias")
    
    def test_search_target_dont_found(self):
        status, value = self.tree.DFS("daniel")
        self.assertFalse(status)
        self.assertEqual(value, None)


    def test_search_path_target_success(self):
        status, value = self.tree.DFS_path("isaias")
        self.assertTrue(status)
        self.assertEqual(value, ['a', 'c', 'm', 'isaias'])
    
        status, value = self.tree.DFS_path("e")
        self.assertTrue(status)
        self.assertEqual(value, ['a', 'b', 'e'])

    def test_search_path_target_dont_found(self):
        status, value = self.tree.DFS_path("daniel")
        self.assertFalse(status)
        self.assertIsNone(value)
    
if __name__=="__main__":
    unittest.main()
    