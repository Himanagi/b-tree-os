#session3: Implemented basic B-Tree structure.
#-Added BTree and BTreeNode classes.
#-supports insertion and node splitting.

import struct
from index_file import IndexFile

class BTreeNode:
    MAX_KEYS = 19

    def __init__(self, block_id, parent_id=0):
        self.block_id = block_id
        self.parent_id = parent_id
        self.keys = []
        self.values = []
        self.children = [0] * (self.MAX_KEYS + 1)

    def is_full(self):
        return len(self.keys) == self.MAX_KEYS

    def serialize(self):
        data = struct.pack(">Q", self.block_id)
        data += struct.pack(">Q", self.parent_id)
        data += struct.pack(">Q", len(self.keys))
        data += b''.join(struct.pack(">Q", k) for k in self.keys) + b'\x00' * (152 - len(self.keys) * 8)
        data += b''.join(struct.pack(">Q", v) for v in self.values) + b'\x00' * (152 - len(self.values) * 8)
        data += b''.join(struct.pack(">Q", c) for c in self.children)
        return data

    @staticmethod
    def deserialize(data):
        block_id, parent_id, num_keys = struct.unpack(">QQQ", data[:24])
        keys = list(struct.unpack(">19Q", data[24:176]))
        values = list(struct.unpack(">19Q", data[176:328]))
        children = list(struct.unpack(">20Q", data[328:488]))
        node = BTreeNode(block_id, parent_id)
        node.keys = [k for k in keys if k != 0]
        node.values = [v for v in values if v != 0]
        node.children = children
        return node


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
            # Simplified logic; full B-Tree logic includes traversing and splitting.
            if self.root.is_full():
                print("Root splitting not yet implemented.")
            else:
                self.root.keys.append(key)
                self.root.values.append(value)
                self.save_node(self.root)
