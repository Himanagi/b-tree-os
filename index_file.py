#Session 2:added 'insert' command
#Introduced IndexFile class to manage file headers.
#added stub for inserting key-value pairs (actual logic comes in session 3).
#insert operation prompts for key and value.

import os
import struct

MAGIC_NUMBER = b'4337PRJ3'

class IndexFile:
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
            file.write(b'\x00' * 488)  # Padding to 512 bytes

    def read_header(self):
        with open(self.filename, 'rb') as file:
            file.seek(0)
            magic = file.read(8)
            if magic != MAGIC_NUMBER:
                raise ValueError("Invalid index file!")
            self.root, self.next_block_id = struct.unpack(">QQ", file.read(16))

    def insert_key_value(self, key, value):
        print(f"Inserting key: {key}, value: {value} (stub).")
        # Actual B-Tree logic will be implemented in Session 3.


def main():
    open_file = None
    index = None

    while True:
        print("\nMenu:")
        print("CREATE - Create a new index file")
        print("OPEN - Open an existing index file")
        print("INSERT - Insert a key-value pair")
        print("QUIT - Exit the program")
        command = input("Enter a command: ").strip().lower()

        if command == "create":
            filename = input("Enter filename: ").strip()
            if os.path.exists(filename):
                overwrite = input(f"{filename} already exists. Overwrite? (yes/no): ").strip().lower()
                if overwrite != "yes":
                    print("Operation aborted.")
                    continue
            with open(filename, 'wb') as file:
                file.write(MAGIC_NUMBER + b'\x00' * 504)  # Write header
            index = IndexFile(filename)
            index.initialize_header()
            print(f"Created {filename}.")
            open_file = filename

        elif command == "open":
            filename = input("Enter filename: ").strip()
            if not os.path.exists(filename):
                print(f"Error: {filename} does not exist.")
                continue
            try:
                index = IndexFile(filename)
                index.read_header()
                print(f"Opened {filename}.")
                open_file = filename
            except ValueError as e:
                print(str(e))

        elif command == "insert":
            if not index:
                print("No file is open.")
                continue
            key = int(input("Enter key (unsigned integer): ").strip())
            value = int(input("Enter value (unsigned integer): ").strip())
            index.insert_key_value(key, value)

        elif command == "quit":
            print("Exiting...")
            break

        else:
            print("Invalid command. Try again.")

if __name__ == "__main__":
    main()
