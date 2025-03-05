import os
from string import ascii_uppercase 

path = r'C:\Users\Lenovo\Desktop\PP2\lab6'

for char in ascii_uppercase:
    file_path = os.path.join(path, f"{char}.txt")
    
    with open(file_path, 'x') as file:
        print(f"Created: {file_path}")
        