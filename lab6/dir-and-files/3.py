import os 

path=r"C:\Users\Lenovo\Desktop\PP2\lab6\dir-and-files"

path_bool=os.access(path, os.F_OK)

if path_bool==False:
    print("Path does not exist")
elif path_bool == True:
    print("Directories:", ', '.join([name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]))
    print("Files:", ', '.join([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]))
    