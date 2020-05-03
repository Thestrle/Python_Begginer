#Write a function that counts the number of times a pattern appears in a given String
# hah in hahahah occurs 3 times
import re

def paperDoll(my_str):
    my_string = ""
    for chr in my_str:
        my_string = my_string + chr * 3
    return my_string

ret_string = paperDoll("Hello")
print(ret_string)

#def laughterCheck(a, b):
#    matches = re.finditer(r'(?=(a{1}))',b)
#    print(matches)
    #results = [int(match.group(1)) for match in matches]

#count = laughterCheck("hah", "hahahah")


def CountOccurrences(string, substring):

    # Initialize count and start to 0
    count = 0
    start = 0

    # Search through the string till
    # we reach the end of it
    while start < len(string):

        # Check if a substring is present from
        # 'start' position till the end
        pos = string.find(substring, start)
        print(pos)

        if pos != -1:
            # If a substring is present, move 'start' to
            # the next position from start of the substring
            start = pos + 1

            # Increment the count
            count += 1
        else:
            # If no further substring is present
            break
    # return the value of count
    return count

num = CountOccurrences("hahahah", "hah")
print(num)
