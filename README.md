# b-tree-os

Interactive B-Tree Index File Manager:

This project implements an interactive program that creates and manages index files using a B-tree data structure. The program allows users to:

-Create, open, and manage index files.
-Insert and search key-value pairs.
-Print or export the B-tree contents.
-Load key-value pairs from a file.

The program adheres to constraints are:
-Storing no more than three nodes in memory at a time.
-Using 512-byte blocks for storage.
-Implementing the B-tree logic with a minimum degree of 10.

Feautures are:
- Create Index Files: Creates a new index file with proper headers and initializes an empty B-tree.
- Open Index Files: Opens and verifes an existing index file based on a magic number.
- Insert Key-Value Pairs: Inserts pairs into the B-tree structure while handling overflows.
- Search Keys: Searches the B-tree for specific keys and retrieves the corresponding values.
- Export Data: Saves the B-tree contents as a CSV file.
- Load Key-Value Pairs: Bulk insert key-value pairs from a CSV file.
- Interactive Menu: Provides an intuitive, menu-driven interface for managing operations.

Setup:
- Install Python (if not already installed)
- Clone the Repository:
git clone https://github.com/Himanagi/b-tree-os.git
cd b-tree-os
- run the program: python index_manager.py
- follow the prompts in the menu to create, open, and manage your index files.

usage: 
- Create: Enter the filename for a new indx file. The program will prompt for overwriting if the file already exists.
- Open: Open an existing index file. Only valid files with the correct magic number will be accepted.
- Insert: Add a key-value pair to the open index file.
-search: Search for a specific key in the index file and retrieve its value.
-Print: Display all key-value pairs stored in the B-tree.
-Load: Bulk load key-value pairs from a CSV file.
-Extract: Save all key-value pairs to a CSV file.
-Quit: Exit the program.


future improvements:
-have a delete operation for the B-tree.
-Optimize file I/O operations for better performance.
-add comprehensive unit tests for all functionalities.
