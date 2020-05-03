a = 3.0
b = 4.0
c= a+b
print (c)
d = 7.0
if (c == d):
    print ("both c and d are same.")

#To reverse a String:
my_string = "abcdef"
print(my_string[::-1])

# format() method for Strings
print ("my {} {} {}".format("dog","black", "is"))
print ("my {0} {2} {1}".format("dog","black", "is"))
print ("my {d} {i} {b}".format(d="dog",b="black", i="is"))

# Example of format string introduced in python3.6
name = "Alok"
age = 27
print(f"My name is {name} and i am {age} years old")

# float formatting follows "{value:width.precision f}"
value = 100/3
print(" value is {:1.3f}".format(value))
print(" value is {:10.3f}".format(value))
print(" value is {v:1.3f}".format(v=value))
