# class Node():
#     def __init__(self, key):
#         self.key = key
#         self.values = []
#         self.left = None
#         self.right = None
        
#     def __len__(self):
#         size = len(self.values)
#         if self.left != None:
#             size += len(self.left)
#         if self.right != None:
#             size += len(self.right)
#         return size
    
#     def lookup_key(key):
#         if self.key == key:
#             return self.values
#         if self.key < key and curr.left != None:
#             left_child = lookup_key(curr.left)
#             return left_child
#         if self.key > key and curr.right != None:
#             right_child = lookup_key(curr.right)
#             return right_child
#         else:
#             return []
                
# class BST():
#     def __init__(self):
#         self.root = None

#     def add(self, key, val):
#         if self.root == None:
#             self.root = Node(key)
#             self.root.values.append(1)  # Initialize count for the first occurrence
#             return

#         curr = self.root
#         while True:
#             if key < curr.key:
#                 # go left
#                 if curr.left == None:
#                     curr.left = Node(key)
#                     curr.left.values.append(1)  # Initialize count for this key
#                     return
#                 curr = curr.left
#             elif key > curr.key:
#                  # go right
#                 if curr.right == None:
#                     curr.right = Node(key)
#                     curr.right.values.append(1)  # Initialize count for this key
#                     return
#                 curr = curr.right              
#             else:
#                 # found it!
#                 assert curr.key == key
#                 break

#         curr.values.append(val)
#     def __dump(self, node):
#         if node == None:
#             return
#         self.__dump(node.right)            # 1
#         print(node.key, ":", node.values)  # 2
#         self.__dump(node.left)             # 3

#     def dump(self):
#         self.__dump(self.root)

# --------------------------------------- partners code ---------------------------------------
class Node():
    def __init__(self, key):
        self.key = key
        self.values = []
        self.left = None
        self.right = None

    def __len__(self):
        size = len(self.values)
        if self.left is not None:
            size += len(self.left)
        if self.right is not None:
            size += len(self.right)
        return size

    # def lookup_key(self, key):  
    def lookup(self, key):
        if self.key == key:
            return self.values
        elif key < self.key and self.left is not None:
            # return self.left.lookup_key(key)  
            return self.left.lookup(key)  
        elif key > self.key and self.right is not None:
            # return self.right.lookup_key(key) 
            return self.right.lookup(key) 
        else:
            return []  

class BST():
    def __init__(self):
        self.root = None

    def add(self, key, val=1): 
        if self.root is None:
            self.root = Node(key)
            self.root.values.append(val) 
            return

        curr = self.root
        while True:
            if key < curr.key:
                # go left
                if curr.left is None:
                    curr.left = Node(key)
                    curr.left.values.append(val) 
                    return
                curr = curr.left
            elif key > curr.key:
                 # go right
                if curr.right is None:
                    curr.right = Node(key)
                    curr.right.values.append(val) 
                    return
                curr = curr.right              
            else:
                # found it!
                assert curr.key == key
                break

        curr.values.append(val)

    def __dump(self, node):
        if node is None:
            return
        self.__dump(node.right)
        print(node.key, ":", node.values)
        self.__dump(node.left)

    def dump(self):
        self.__dump(self.root)
        
    def __getitem__(self, key):
        return self.root.lookup(key)