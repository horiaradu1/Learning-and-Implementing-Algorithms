import sys
import random

# This will have a large impact on performance, try playing with it
MAX_LEVEL = 20

class node:
    def __init__(self, value, priority,levels):
        self.priority = priority
        self.value = value
        self.height = levels
        self.next = [None] * levels

class skiplist:
    def __init__(self):
        self.levels = 1
        self.size = 0
        self.header = node(None,sys.maxsize,MAX_LEVEL)
        for i in range(MAX_LEVEL):
            self.header.next[i] = self.header
            
    def is_empty(self):
        return self.size <= 0
        
    # Returns the last node with priority not less than 'priority'
    # The above line purposefully does not say 'or equal' as returning
    # the last node in the case of duplicates makes the contains function fail
    #
    # Records in 'updates' the nodes along the path that would need updating if a node to
    # their right on their level were to be inserted e.g. the nodes at which the decision
    # to go 'down' is made
    def search(self, priority, updates):
        node = self.header
        level = MAX_LEVEL
        while (level > 0):
            level = level - 1
            
            # TODO we now need to scan along this level until the 'next
            # priority is not less than the priority we are searching for.
            # (Hint: the next node at this level is currently in node.next[level]
            
            # Record the node where we go down at a particular level
            if (not updates == None):
                updates[level] = node
        
        return node
        
    def insert(self, value, priority):
        updates = [None] * MAX_LEVEL
        insert_at = self.search(priority, updates)
        
        # TODO create a new_node with a random number of levels
        # where the chance of having n levels is 1/2^n e.g. flip
        # a coin for each level.  (Hint: use random.randint(0,1))
        
        new_node = None
        
        for i in range(levels):
            new_node.next[i] = updates[i].next[i]
            updates[i].next[i] = new_node
            
        self.size = self.size + 1
        
    def contains(self, value, priority):
        node = self.search(priority, None).next[0]
        while (node.priority == priority and (not node.value == None) and (not node.value == value)):
            node = node.next[0]
        return (node.priority == priority and (not node.value == None) and node.value == value)
        
    def pop_min(self):
        min = self.header.next[0]
        res = min.value
        
        # TODO what do we need to do to repair the Skip List
        # to remove the min node?  Hint: which nodes are followed by min and
        # what should they now be followed by
        
        self.size = self.size - 1
        return res
        
    # There are probably nicer ways to print a skiplist
    def print(self):
    
        node = self.header
        sys.stdout.write("(%s,%s,%s)\n" % (node.value, node.priority, node.height))
        node = node.next[0]
        while (not node == self.header):
            sys.stdout.write("(%s,%s,%s)\n" % (node.value, node.priority, node.height))
            node = node.next[0]
        
