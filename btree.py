#session 4: Fixed root splitting logic.
#Added `split_node` method to handle node splits.
#updated `insert` to handle root splitting correctly.

#date: DEC7, time 12;40 AM

class BTree:
    def __init__(self, index_file):
        self.index_file = index_file
        self.root = None

    def load_root(self):
        if self.index_file.root == 0:
            self.root = None
        else:
            data = self.index_file.read_node(self.index_file.root)
            self.root = BTreeNode.deserialize(data)

    def save_node(self, node):
        self.index_file.write_node(node.block_id, node.serialize())

    def split_node(self, node):
        # Split the current node and return the new node
        mid_index = len(node.keys) // 2
        mid_key = node.keys[mid_index]
        mid_value = node.values[mid_index]

        #create a new node with the second half of keys/values
        new_block_id = self.index_file.allocate_block()
        new_node = BTreeNode(new_block_id, node.parent_id)
        new_node.keys = node.keys[mid_index + 1:]
        new_node.values = node.values[mid_index + 1:]
        new_node.children = node.children[mid_index + 1:]

        # Update the original node to keep only the first half
        node.keys = node.keys[:mid_index]
        node.values = node.values[:mid_index]
        node.children = node.children[:mid_index + 1]

        self.save_node(node)
        self.save_node(new_node)

        return mid_key, mid_value, new_node.block_id

    def insert(self, key, value):
        if self.root is None:
            block_id = self.index_file.allocate_block()
            self.root = BTreeNode(block_id)
            self.root.keys.append(key)
            self.root.values.append(value)
            self.index_file.root = block_id
            self.index_file.write_node(0, self.index_file.read_node(0))  # Update header
            self.save_node(self.root)
        else:
            current_node = self.root
            # Simplified logic for navigating and inserting into the tree
            while current_node.children[0] != 0:  # If not a leaf node
                for i, k in enumerate(current_node.keys):
                    if key < k:
                        child_block_id = current_node.children[i]
                        break
                else:
                    child_block_id = current_node.children[len(current_node.keys)]
                current_node = BTreeNode.deserialize(self.index_file.read_node(child_block_id))

            # Insert the key into the leaf node
            current_node.keys.append(key)
            current_node.values.append(value)
            current_node.keys.sort()
            current_node.values.sort()
            self.save_node(current_node)

            # Handle splitting if necessary
            while current_node.is_full():
                mid_key, mid_value, new_block_id = self.split_node(current_node)

                if current_node == self.root:
                    # If splitting the root, create a new root
                    new_root_block_id = self.index_file.allocate_block()
                    new_root = BTreeNode(new_root_block_id)
                    new_root.keys = [mid_key]
                    new_root.values = [mid_value]
                    new_root.children[0] = current_node.block_id
                    new_root.children[1] = new_block_id

                    self.root = new_root
                    self.index_file.root = new_root_block_id
                    self.save_node(new_root)
                    break
                else:
                    # Update parent node
                    parent_block_id = current_node.parent_id
                    parent_node = BTreeNode.deserialize(self.index_file.read_node(parent_block_id))
                    parent_node.keys.append(mid_key)
                    parent_node.values.append(mid_value)
                    parent_node.children[parent_node.keys.index(mid_key) + 1] = new_block_id
                    self.save_node(parent_node)
                    current_node = parent_node
