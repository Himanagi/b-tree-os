#session 3: Added B-Tree integration
#supports insert and basic file operations.
# future sessions will refine B-Tree logic.

from index_file import IndexFile
from btree import BTree

def main():
    index = None
    btree = None

    while True:
        print("\nMenu:")
        print("CREATE - Create a new index file")
        print("OPEN - Open an existing index file")
        print("INSERT - Insert a key-value pair")
        print("QUIT - Exit the program")
        command = input("Enter a command: ").strip().lower()

        if command == "create":
            filename = input("Enter filename: ").strip()
            index = IndexFile(filename)
            with open(filename, 'wb') as f:
                f.write(b'\x00' * IndexFile.BLOCK_SIZE)  # Placeholder for header
            index.initialize_header()
            btree = BTree(index)
            print(f"Created {filename}.")

        elif command == "open":
            filename = input("Enter filename: ").strip()
            try:
                index = IndexFile(filename)
                index.read_header()
                btree = BTree(index)
                btree.load_root()
                print(f"Opened {filename}.")
            except ValueError as e:
                print(str(e))

        elif command == "insert":
            if btree is None:
                print("No file is open.")
                continue
            key = int(input("Enter key (unsigned integer): ").strip())
            value = int(input("Enter value (unsigned integer): ").strip())
            btree.insert(key, value)

        elif command == "quit":
            print("Exiting...")
            break

        else:
            print("Invalid command. Try again.")

if __name__ == "__main__":
    main()
