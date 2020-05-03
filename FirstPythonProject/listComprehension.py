mystring = "alok"
mylist =[]
for char in mystring:
    mylist.append(char)
print(mylist)

print("*****************")

newlist = [letters for letters in mystring]
print(newlist)

numlist = [num**2 for num in range(10) if num%2==0]
print(numlist)

numlist = [x if x%2==0 else x**2 for x in range(10)]
print(numlist)
