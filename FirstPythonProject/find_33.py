# if recieved list contains 3,3 in a sequence return true else False

def has_33(nums):
    for i in range(0,len(nums)-1):
        if nums[i] == 3 and nums[i+1] == 3:
            True
        #if nums[i:i+2] == [3,3] gives same output

lis = [1,2,3,4,5,6,7,8,9]

#Below method will exlcude any number starting from idex with value  6 till index with value 9
# and will return sum of remaining list values.
def summer_69(nums):
    i_start =0
    i_end = -1
    flag = False
    for i in range(len(nums)-1):
        if 6 in nums:
            if nums[i] == 6:
                i_start = i
                flag = True
            if nums[i] == 9 and flag:
                i_end = i+1
            new_list = nums[:i_start] + nums[i_end:]
        else:
            new_list = nums

    return sum(new_list)

print(summer_69([1,2,3,4,5,6,7,8,9,11]))
print(summer_69([1,2,3,4,5]))
