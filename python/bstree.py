import config

global height_max
global no_inserts
global duplicates
global total_finds_counter
global no_finds
global no_nodes
height_max = 0
no_inserts = 0
duplicates = 0
total_finds_counter = 0
no_finds = 0
no_nodes = 0

class bstree:
    def __init__(self):
        self.verbose = config.verbose

    def size(self):
        if (self.tree()):
            return 1 + self.left.size() + self.right.size()
        return 0
        
    def tree(self):
        # This counts as a tree if it has a field self.value
        # it should also have sub-trees self.left and self.right
        return hasattr(self, 'value')

    def tree_left(self):
        return hasattr(self, 'left')

    def tree_right(self):
        return hasattr(self, 'right')
        
    def insert(self, value, height = 0):
        if (self.tree()):
            # If tree is not NULL then insert into the correct sub-tree
            # Ignore errors, as self.value can not get here until it gets through the creation of a new node
            global no_inserts
            global duplicates
            # If value is smaller that parent value, go left
            if self.value > value:
                # If its already a bstree, insert the value
                if self.tree_left():
                    no_inserts = no_inserts + 1
                    self.left.insert(value, height = height + 1)
                # If its not, first create it as a bstree, then insert the value
                else:
                    self.left = bstree()
                    no_inserts = no_inserts + 1
                    self.left.insert(value, height = height + 1)
            # If value is bigger that parent value, go right
            elif self.value < value:
                # If its already a bstree, insert the value
                if self.tree_right():
                    no_inserts = no_inserts + 1
                    self.right.insert(value, height = height + 1)
                # If its not, first create it as a bstree, then insert the value
                else:
                    self.right = bstree()
                    no_inserts = no_inserts + 1
                    self.right.insert(value, height = height + 1)
            else:
                # If the values are equal, nothing happens, just counting the duplicates for stats
                duplicates = duplicates + 1
        else:
            # Otherwise create a new node containing the value
            # And calculate the max height
            global height_max
            global no_nodes
            no_nodes = no_nodes + 1
            if height_max < height:
                height_max = height
            self.value = value
        
    def find(self, value, counter = 0):
        if self.tree():
            global total_finds_counter
            global no_finds
            # Find function
            # Looks first if the value is found
            if self.value == value:
                total_finds_counter = total_finds_counter + counter
                no_finds = no_finds + 1
                return True
            # If not starts checking left or right, recursively, depending on the value
            # Untill it either returns True, or the value is not found
            elif self.value > value and self.tree_left():
                return self.left.find(value, counter = counter + 1)
            elif self.value < value and self.tree_right():
                return self.right.find(value, counter = counter + 1)
            else:
                return False
        return False
        
    # You can update this if you want
    def print_set_recursive(self, depth):
        if (self.tree()):
            for i in range(depth):
                print(" ", end='')
            print("%s" % self.value)
            self.left.print_set_recursive(depth + 1)
            self.right.print_set_recursive(depth + 1)
            
    # You can update this if you want
    def print_set(self):
        print("Tree:\n")
        self.print_set_recursive(0)
        
    def print_stats(self):
        # Print stats
        global height_max
        global duplicates
        global total_finds_counter
        global no_finds
        global no_nodes
        print("Height of the Binary Search Tree: " + str(height_max))
        print("Number of inserts: " + str(no_inserts))
        print("Number of duplicates: " + str(duplicates))
        print("Number of nodes: " + str(no_nodes))
        print("Average number of comparisons per find: " + str(total_finds_counter / no_finds))
