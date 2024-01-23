import unittest 

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
    
    def __str__(self):
        return str(self.data)

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, new_node):
        if not self.head:
            self.head = new_node
        if self.tail:
            self.tail.next = new_node
        self.tail = new_node
        
    def dequeue(self):
        node = self.head
        if node:
            self.head = node.next
        return node

    def __str__(self):
        queue = "< "
        for node in self:
            queue += str(node) + str(", " if node.next else "")
        return queue + " >"

    def __iter__(self):
        node = self.head
        while node:
            yield node
            node = node.next

def BFS(graph, root, item):
    queue = Queue( )
    queue.enqueue(Node(root))
    explored = [root]
    while queue.head:
        node = queue.dequeue()
        children = graph.get(node.data, [])
        for child in children:
            if child == item:
                return True
            if child in explored:
                continue 
            explored.append(child)
            queue.enqueue(Node(child))
    return False

def BFS_path(graph, root, item):
    queue = Queue( )
    queue.enqueue(Node([root]))
    explored = [root]
   
    while queue.head:
        node = queue.dequeue()
        children = graph.get(node.data[-1], [])
        for child in children:
            path = node.data[::]
            path.append(child)
            if child == item:
                return True, path
            if child in explored:
                continue
            explored.append(child)
            queue.enqueue(Node(path))
    return False, None
        

class QueueTest(unittest.TestCase):

    def setUp(self) -> None:
        self.queue = Queue()
        return super().setUp()
    
    def test_empty_queue(self):
        queue_str = str(self.queue)
        expected = "<  >"
        self.assertEqual(queue_str, expected)

    def test_insert_objects(self):
        self.queue.enqueue(Node(1))
        self.queue.enqueue(Node("2"))
        self.queue.enqueue(Node("hola"))
        queue_str = str(self.queue)
        expected = "< 1, 2, hola >"
        self.assertEqual(queue_str, expected)

    def test_delete_objects(self):
        self.queue.enqueue(Node(1))
        self.queue.enqueue(Node("2"))
        self.queue.enqueue(Node("hola"))
        node = self.queue.dequeue()
        expected = 1
        self.assertEqual(node.data, expected)

        self.queue.dequeue()
        queue_str = str(self.queue) 
        expected = "< hola >"
        self.assertEqual(queue_str, expected)

    def test_delete_empty_queue(self):
        node = self.queue.dequeue()
        self.assertIsNone(node)

class BFSTest(unittest.TestCase):

    def setUp(self) -> None:
        self.tree = {
            "a": ["b", "c"],
            "b": ["d", "e","f", "g"],
            "c": ["h", "i","j","k","l","m"],
            "f": ["o", "p"],
            "h": ["r", "s"],
            "k": ["t"],
            "o": ["1"],
            "p": ["z"],
            "r": ["y"],
            "s": ["x"],
            "t": ["u"],
            "u": ["isaias"]
        }
        return super().setUp()

    def test_search_target_success(self):
        output = BFS(self.tree,"a", "isaias")
        self.assertTrue(output)
            

    def test_search_path_target_success(self):
   
        status, path = BFS_path(self.tree, "a", "1")
        self.assertTrue(status)
        self.assertEqual(path,['a', 'b', 'f', 'o', '1'])
        status, path = BFS_path(self.tree, "a", "isaias")
        self.assertTrue(status)
        self.assertEqual(path,['a', 'c', 'k', 't', 'u', 'isaias'])
        self.tree["k"].append("isaias")
        status, path = BFS_path(self.tree, "a", "isaias")
        self.assertTrue(status)
        self.assertEqual(path,['a', 'c', 'k', 'isaias'])
        
        self.tree["b"].append("isaias")
        status, path = BFS_path(self.tree, "a", "isaias")
        self.assertTrue(status)
        self.assertEqual(path,['a', 'b', 'isaias'])
        
        self.tree["a"].append("isaias")
        status, path = BFS_path(self.tree, "a", "isaias")
        self.assertTrue(status)
        self.assertEqual(path,['a', 'isaias'])
    
    def test_search_target_dont_found(self):
        output = BFS(self.tree,"a", "daniel")
        self.assertFalse(output)

    def test_search_path_target_dont_found(self):
        status, value = BFS_path(self.tree, "a", "daniel")
        self.assertFalse(status)
        self.assertIsNone(value)


class BFSTest(unittest.TestCase):

    def setUp(self) -> None:
        self.graph = {
            "s": ["a", "b"],
            "a": ["c"],
            "b": ["c", "d"],
            "c": ["e"],
            "d": ["f"]
        }
        return super().setUp()

    def test_search_target_success(self):
        output = BFS(self.graph,"s", "d")
        self.assertTrue(output)
            

    def test_search_path_target_success(self):
        status, path = BFS_path(self.graph,"s", "d")
        self.assertTrue(status)
        self.assertEqual(path,['s', 'b', 'd'])
        status, path = BFS_path(self.graph,"s", "d")
        self.assertTrue(status)
        self.assertEqual(path,['s', 'b', 'd'])
        status, path = BFS_path(self.graph,"s", "e")
        self.assertTrue(status)
        self.assertEqual(path,['s', 'a', 'c', 'e'])

if __name__=="__main__":
    unittest.main()
   
    