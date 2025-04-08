import os

path= r"C:\Users\Lenovo\Desktop\PP2\lab6\11.py"

path_bool=os.access(path,os.F_OK)

if path_bool == False:
     print('Path does not exist')
elif path_bool == True:
    os.remove(path)
    print("File has been removed")
    