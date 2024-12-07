# aession 3: Updated file operations for B-Tree support.
#Added support for block-based file access.
# added methods to write/read nodes from file.

import os
import struct

MAGIC_NUMBER = b'4337PRJ3'

class IndexFile:
    BLOCK_SIZE = 512

    def __init__(self, filename):
        self.filename = filename
        self.root = 0
        self.next_block_id = 1

    def initialize_header(self):
        with open(self.filename, 'r+b') as file:
            file.seek(0)
            file.write(MAGIC_NUMBER)
            file.write(struct.pack(">Q", self.root))
            file.write(struct.pack(">Q", self.next_block_id))
            file.write(b'\x00' * (self.BLOCK_SIZE - 24))  #Padding to 512 bytes

    def read_header(self):
        with open(self.filename, 'rb') as file:
            file.seek(0)
            magic = file.read(8)
            if magic != MAGIC_NUMBER:
                raise ValueError("Invalid index file!")
            self.root, self.next_block_id = struct.unpack(">QQ", file.read(16))

    def write_node(self, block_id, data):
        with open(self.filename, 'r+b') as file:
            file.seek(block_id * self.BLOCK_SIZE)
            file.write(data)

    def read_node(self, block_id):
        with open(self.filename, 'rb') as file:
            file.seek(block_id * self.BLOCK_SIZE)
            return file.read(self.BLOCK_SIZE)

    def allocate_block(self):
        block_id = self.next_block_id
        self.next_block_id += 1
        with open(self.filename, 'r+b') as file:
            file.seek(16)
            file.write(struct.pack(">Q", self.next_block_id))
        return block_id
