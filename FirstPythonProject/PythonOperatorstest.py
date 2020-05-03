myString = "Print every word in this sentence that has Even number of letters"
my_list = myString.split()
print(my_list)
for word in my_list:
    if len(word)%2 == 0:
        print(word)
