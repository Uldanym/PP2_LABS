import os

path=r"C:\Users\Lenovo\Desktop\PP2\lab6\dir-and-files"

print("All:", [name for name in os.listdir(path)])
print("Folders:", [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))])
print("Files:", [name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
