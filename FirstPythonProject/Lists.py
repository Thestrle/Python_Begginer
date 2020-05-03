my_string = 'String'
print(list(my_string))

# method to reverse the string
def reverse(s):

    str = ""
    for i in s:
        str = i + str
    return str
# End of reverse method this can be achieved by my_string[::-1] too

rev_string = reverse(my_string)
print(rev_string)
