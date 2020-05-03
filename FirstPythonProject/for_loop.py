my_list = [(1,2), (3,4), (5,6)]

for item in my_list:
    print(item)
# Unpacking in List with Tuple as item
for a,b in my_list:
    print(a)

for a,b in my_list:
    print(b)

#my_list = [(1,2,7), (3,4), (5,6,8)]
#for a,b,c in my_list: will rncounter err as number of item not same in all tuple
#    print(a)

my_dict = { 1:'a', 2:'b', 3:'c'}
for item in my_dict:
    print (item)
for item in my_dict.items():
    print (item)
for a,b in my_dict.items():
    print (a,b)
