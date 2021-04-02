import os

# Look for your absolute directory path
file_path = os.path.abspath(__file__)
# Or: file_path = os.path.join(absolute_path, 'folder', 'my_file.py')
# file_path = absolute_path + "/folder/my_file.py"
print(file_path)
