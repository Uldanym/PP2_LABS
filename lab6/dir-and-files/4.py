with open (r'C:\Users\Lenovo\Desktop\PP2\lab6\dir-and-files\text.txt', 'r') as file:
        x = len(file.readlines())
        print("Number of lines:", x)