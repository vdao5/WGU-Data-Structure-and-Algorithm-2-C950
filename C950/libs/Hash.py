"""
HashSet:
    self-addjusting capacity (rehashing)
    store HashNode objects in buckets
        To prevent collisions, HashNode objects can be linked together in buckets to form a linked list.

    insert O(1) average, O(n) worst case
    remove O(1) average, O(n) worst case
    lookup O(1) average, O(n) worst case

HashMap:
    built on top of HashSet, inherits lookup O(1) average
    store HashNode objects in a BST (beside the HashSet buckets)
        HashNode objects are stored in a BST to allow for iteration in order
        HashNode objects can be sorted by key (default) or value.
    
    insert O(log n)
    remove O(log n)
    lookup O(1)
    peek (min/max) O(1)
    sorted O(n)
"""
from .Tree import TreeNode, BST
from copy import deepcopy

class HashNode(TreeNode):
    def __init__(self, key, value = None):
        TreeNode.__init__(self, value)

        self.key = key
        self.link = None
    
    def __hash__(self) -> int:
        return hash(self.key)
    
class HashSet():
    LOAD_FACTOR = 0.75

    def __init__(self, capacity=8):
        self.capacity = capacity
        self.size = 0
        self.buckets = [None] * capacity

    def __len__(self):
        return self.size
    
    def __contains__(self, key):
        return self._get_node(key) is not None
    
    def __iter__(self):
        for node in self.buckets:
            while node is not None:
                yield node
                node = node.link

    def keys(self):
        keys = []
        for node in self:
            keys.append(node.key)
        return keys
    
    def _get_node(self, key):
        idx = hash(key) % self.capacity
        node = self.buckets[idx]
        while node is not None:
            if node.key == key:
                return node
            node = node.link
        return None

    def _rehash(self):
        new_capacity = self.capacity * 2
        new_buckets = [None] * new_capacity
        for node in self.buckets:
            while node is not None:
                link = node.link

                idx = hash(node.key) % new_capacity
                node.link = new_buckets[idx]
                new_buckets[idx] = node

                node = link
        self.buckets = new_buckets
        self.capacity = new_capacity

    def _rehash_check(self):
        if self.size / self.capacity >= self.LOAD_FACTOR:
            self._rehash()

    def insert(self, key):
        idx = hash(key) % self.capacity
        node = self.buckets[idx]
        while node is not None:
            if node.key == key:
                return node
            node = node.link

        node = HashNode(key)
        node.link = self.buckets[idx]
        self.buckets[idx] = node
        self.size += 1
        self._rehash_check()

        return node

    def remove(self, key):
        idx = hash(key) % self.capacity
        node = self.buckets[idx]
        prev = None
        while node is not None:
            if node.key == key:
                if prev is None:
                    self.buckets[idx] = node.link
                else:
                    prev.link = node.link

                self.size -= 1
                return node
            prev = node
            node = node.link
        
        return None
    
class HashMap(BST, HashSet):
    def __init__(self, capacity=8, order_by = 'key', default_value = None):
        HashSet.__init__(self, capacity)
        BST.__init__(self, order_by)
        self.default_value = default_value

    def __getitem__(self, key):
        return self.get_value(key)
    
    def __setitem__(self, key, value):
        node = HashSet._get_node(self, key)
        if node is not None:
            node.value = value
        else:
            self.insert(key, value)

    def get_value(self, key):
        node = HashSet._get_node(self, key)
        if node is None and self.default_value is not None:
            node = self.insert(key, deepcopy(self.default_value))
        return node.value if node is not None else None
    
    def __iter__(self):
        node = self.begin_inorder
        while node is not None:
            yield node
            node = node.next

    @property
    def begin(self):
        return self.begin_inorder
    
    @property
    def end(self):
        return self.end_inorder
    
    def keys(self):
        keys = []
        for node in self:
            keys.append(node.key)
        return keys

    def values(self):
        values = []
        for node in self:
            values.append(node.value)
        return values
    
    def items(self):
        items = []
        for node in self:
            items.append((node.key, node.value))
        return items
    
    def insert(self, key, value = None):
        size_before_insert = self.size
        node = HashSet.insert(self, key)

        node.value = value
        if hasattr(node.value, 'owner'):
            node.value.owner = node

        if size_before_insert < self.size:
            BST.insert_node(self, node)

        return node
    
    def remove(self, key):
        node = HashSet.remove(self, key)
        if node is not None:
            if hasattr(node.value, 'owner'):
                node.value.owner = None
            BST.remove_node(self, node)

        return node
    
def watch(*attrs):
    def _watch(cls):
        class Watch(cls):
            watch_by = attrs
            def __init__(self, *args, **kargs):
                self.owner = None
                super().__init__(*args, **kargs)

            def __setattr__(self, name, value):
                object.__setattr__(self, name, value)

                if self.owner is not None and name in Watch.watch_by:
                    self.owner.self_adjust()
            
            def __lt__(self, other):
                for attr in Watch.watch_by:
                    if getattr(self, attr) < getattr(other, attr):
                        return True
                    elif getattr(self, attr) > getattr(other, attr):
                        return False
                return False

        return Watch
    return _watch
