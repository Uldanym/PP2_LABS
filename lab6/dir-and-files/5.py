list1=list(map(str,input().split()))

file_name = 'new.txt'

with open(file_name, 'w') as file:
    file.write(str(list1))
    
file.closed()