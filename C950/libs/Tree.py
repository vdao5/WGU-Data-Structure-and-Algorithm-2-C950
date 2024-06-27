"""
BST:
    implemented as a self-balancing AVL tree
    added custom self-adjustment to keep track of inorder traversal (sort, heap peek)
"""

class TreeNode:
    def __init__(self, value):
        self.initialize()
        self.value = value

    def initialize(self):
        self.tree = None
        self.parent = None
        self.left = None
        self.right = None
        self.predecessor = None
        self.successor = None
        self.height = 0

    @property
    def next(self):
        return self.successor
    
    @property
    def prev(self):
        return self.predecessor

    def self_adjust(self):
        if self.tree is not None:
            self.tree.self_adjust(self)
    
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)

        if self.tree is not None and name == self.tree.order_by:
            self.tree.self_adjust(self)
        
    def get_predecessor(self):
        if self.left is not None:
            node = self.left
            while node.right is not None:
                node = node.right
            return node
        else:
            node = self
            while node.parent is not None and node.parent.left is node:
                node = node.parent
            return node.parent
        
    def get_successor(self):
        if self.right is not None:
            node = self.right
            while node.left is not None:
                node = node.left
            return node
        else:
            node = self
            while node.parent is not None and node.parent.right is node:
                node = node.parent
            return node.parent
        
    def link_inorder(self):
        self.predecessor = self.get_predecessor()
        self.successor = self.get_successor()

        if self.predecessor is not None:
            self.predecessor.successor = self
        else:
            self.tree.begin_inorder = self

        if self.successor is not None:
            self.successor.predecessor = self
        else:
            self.tree.end_inorder = self
    
    def unlink_inorder(self):
        if self.predecessor is not None:
            self.predecessor.successor = self.successor
        else:
            self.tree.begin_inorder = self.successor

        if self.successor is not None:
            self.successor.predecessor = self.predecessor
        else:
            self.tree.end_inorder = self.predecessor
            
        self.predecessor = None
        self.successor = None
        
    @staticmethod
    def get_height(node):
        if node is None:
            return -1
        return node.height
    
    def get_balance(self):
        return TreeNode.get_height(self.left) - TreeNode.get_height(self.right)
    
    def update_height(self):
        self.height = max(TreeNode.get_height(self.left), TreeNode.get_height(self.right)) + 1
    
    def set_left(self, left):
        self.left = left
        if left is not None:
            left.parent = self
        self.update_height()
        
    def set_right(self, right):
        self.right = right
        if right is not None:
            right.parent = self
        self.update_height()

    def replace_child(self, current_child, new_child):
        if self.left is current_child:
            return self.set_left(new_child)
        elif self.right is current_child:
            return self.set_right(new_child)
          
        return False

class BST():
    def __init__(self, order_by = 'value'):
        self.root = None
        self.begin_inorder = None
        self.end_inorder = None
        self.order_by = order_by

    def _lt(self, node1, node2):
        return node1.__getattribute__(self.order_by) < node2.__getattribute__(self.order_by)
        
    def rotate_left(self, node):
        right_left_child = node.right.left

        if node.parent is not None:
            node.parent.replace_child(node, node.right)
        else:
            self.root = node.right
            self.root.parent = None

        node.right.set_left(node)
        node.set_right(right_left_child)
        
        return node.parent

    def rotate_right(self, node):
        left_right_child = node.left.right

        if node.parent is not None:
            node.parent.replace_child(node, node.left)
        else:
            self.root = node.left
            self.root.parent = None

        node.left.set_right(node)
        node.set_left(left_right_child)
        
        return node.parent
    
    def self_adjust(self, node):
        predecessor = node.predecessor
        successor = node.successor

        # correct order: predecessor < node < successor
        # so if 
        #   node < predecessor or 
        #   successor < node, 
        # then node is not in correct order

        if( (predecessor is not None and self._lt(node, predecessor)) or
            (successor is not None and self._lt(successor, node)) ):
            self.remove_node(node)
            self.insert_node(node)

    def self_balance(self, node):
        node.update_height()
        
        if node.get_balance() == -2:
            if node.right.get_balance() == 1:
                self.rotate_right(node.right)
                
            return self.rotate_left(node)
        elif node.get_balance() == 2:
            if node.left.get_balance() == -1:
                self.rotate_left(node.left)
                
            return self.rotate_right(node)
        return node

    def insert_node(self, node):
        if node is None:
            return
        
        node.initialize()
        node.tree = self

        if self.root is None:
            node.parent = None
            self.root = node
        else:
            current_node = self.root
            while current_node is not None:
                #if node.value < current_node.value:
                if self._lt(node, current_node):
                    if current_node.left is None:
                        current_node.left = node
                        node.parent = current_node
                        current_node = None
                    else:
                        current_node = current_node.left
                else:
                    if current_node.right is None:
                        current_node.right = node
                        node.parent = current_node
                        current_node = None
                    else:
                        current_node = current_node.right

            
            parent = node.parent
            while parent is not None:
                self.self_balance(parent)
                parent = parent.parent


        node.link_inorder()
        return node
                           
    def remove_node(self, node):
        if node is None:
            return
            
        parent = node.parent
        successor_node = node.successor
        node.unlink_inorder()

        if node.left is not None and node.right is not None:
            successor_node.set_left(node.left)
            if successor_node.parent is not node:
                successor_node.parent.replace_child(successor_node, successor_node.right)
                successor_node.set_right(node.right)
                
            if parent is None:
                self.root = successor_node
                successor_node.parent = None
            else:
                parent.replace_child(node, successor_node)

            self.self_balance(successor_node)

        elif node is self.root:
            if node.left is not None:
                 self.root = node.left
            else:
                 self.root = node.right

            if self.root is not None:
                 self.root.parent = None

        elif node.left is not None:
            parent.replace_child(node, node.left)

        else:
            parent.replace_child(node, node.right)


        while parent is not None:
            self.self_balance(parent)            
            parent = parent.parent

        node.initialize()

    def remove_node2(self, node):
        if node is None:
            return