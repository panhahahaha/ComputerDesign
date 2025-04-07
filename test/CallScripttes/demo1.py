class Node:
    def __init__(self):
        self.next = None


n1 = Node()
n2 = Node()
n1.next = n2
n2.next = n1
print(n1)
