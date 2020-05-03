#Write a Fuunction that takes a list of Integers and returns True if it contains (0,0,7) in od=rder]
def spyGame(nums):
    code = [0,0,7, 'x']
    for num in nums:
        if num == code[0]:
            code.pop(0)

    return len(code) == 1

print(spyGame([0,0,7,1,2]))
print(spyGame([0,1,0,1,2,7]))
print(spyGame([7,0,0,1,2]))
