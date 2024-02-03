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
        if position < 0:
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
        if position < 0:
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

    def push(self, node):
        node.next = self.head
        self.head = node

    def pop(self):
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
        node = None if not self.head else self.head.next
        while node:
            output += str(node) + (", " if node.next else "")
            node = node.next
        return output + "]"

    def __iter__(self):
        node = self.head
        while node:
            yield node.data
            node = node.next
