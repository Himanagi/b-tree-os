# Session 4:added debugging print statements for testing root splitting.

#date: DEC7, time 12;40 AM

def main():
    index = None
    btree = None

    while True:
        print("\nMenu:")
        print("CREATE - Create a new index file")
        print("OPEN - Open an existing index file")
        print("INSERT - Insert a key-value pair")
        print("PRINT - Print the current B-Tree structure")
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

        elif command == "print":
            if btree is None or btree.root is None:
                print("No B-Tree loaded.")
            else:
                print("Root Node:")
                print(f"Keys: {btree.root.keys}")
                print(f"Values: {btree.root.values}")
                print(f"Children: {btree.root.children}")

        elif command == "quit":
            print("Exiting...")
            break

        else:
            print("Invalid command. Try again.")

if __name__ == "__main__":
    main()
