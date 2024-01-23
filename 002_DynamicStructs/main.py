class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
    
    def __str__(self):
        return str(self.data)

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, Node):
        if self.head != None:
            self.tail.next = Node
            self.tail = Node
        else:
            self.head = Node
            self.tail = Node

    def insert(self, position, new_node):
        current = self.head
        next = None if not self.head else self.head.next
        prev = None
        count = 0 
        if  position < 0:
            raise IndexError()

        while current:
           if count == position:
            if not prev:
                self.head = new_node
                new_node.next = current
            else:
                prev.next = new_node
                new_node.next = current
            return
           prev = current
           current = next
           next = None if not next else next.next
           count += 1

        if count < position:
            raise IndexError()

    def delete(self, position):
        current = self.head
        next = None if not self.head else self.head.next
        prev = None
        count = 0 
        if  position < 0:
            raise IndexError()

        while current:
           if count == position:
            if not prev:
                self.head = next
            else:
                prev.next = next
            return
           prev = current
           current = next
           next = None if not next else next.next
           count += 1

        if count < position:
            raise IndexError()

    def push (self, node):
        node.next = self.head
        self.head = node 

    def pop (self):
        node = self.head
        self.head = self.head.next if self.head else None
        return node

    def enqueue(self, node):
        self.append(node)

    def dequeue(self):
        return self.pop()

    def __str__(self):
        output = "["
        output += "" + str(self.head) + ", " if self.head else ""
        node =  None if not self.head else self.head.next
        while node:
            output += str(node) + (", " if node.next else "")
            node = node.next
        return output+ "]"

    def __iter__(self):
        node = self.head
        while node:
            yield node.data
            node = node.next


# Create an empty linked list
my_list = LinkedList()
# Create nodes and link them together
my_list.append(Node(0))
my_list.append(Node(1))
my_list.append(Node(2))
my_list.append(Node(3))
my_list.append(Node(4))
my_list.append(Node(5))
my_list.append(Node(6))
my_list.insert(0, Node("position 0"))
my_list.insert(1, Node("position 1"))
my_list.insert(2, Node("position 2"))
my_list.insert(3, Node("position 3"))
my_list.insert(9, Node("position 9"))

print(my_list)

my_list.delete(0)
my_list.delete(2)
my_list.delete(7)
my_list.delete(1)
my_list.delete(0)
my_list.delete(0)
my_list.delete(0)
print(my_list)

my_list.delete(0)
my_list.delete(0)
my_list.delete(0)
my_list.delete(0)
my_list.delete(0)
my_list.delete(0)
print(my_list)

# my_list.push(Node(1))
# my_list.push(Node(2))
# my_list.push(Node(3))
# my_list.push(Node(4))
# print(my_list)

# my_list.pop()
# my_list.pop()
# print(my_list)
# my_list.pop()
# print(my_list)
# my_list.pop()
# print(my_list)
# my_list.pop()
# my_list.pop()
# print(my_list)

# print(my_list)
# my_list.enqueue(Node(0))
# my_list.enqueue(Node(1))
# my_list.enqueue(Node(2))
# my_list.enqueue(Node(3))
# my_list.enqueue(Node(4))
# my_list.enqueue(Node(5))
# print(my_list)
# print(my_list.dequeue(), my_list)
# print(my_list.dequeue(), my_list)
# print(my_list.dequeue(), my_list)