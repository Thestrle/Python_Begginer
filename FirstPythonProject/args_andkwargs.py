# *args returns and accepts tuple or variable number of arguments
# **kwargs returns and accepts dictionaries or variable number of arguments
# While passing *args and **kwargs both in a function the order of recieving and sending params should be same
#e.g. myfunc(10,20,30,40,fruit='apple',veg='tomato') def myfunc(*args,**kwargs) correct
#e.g. myfunc(10,20,30,40,fruit='apple',veg='tomato',50) def myfunc(*args,**kwargs) wrong
