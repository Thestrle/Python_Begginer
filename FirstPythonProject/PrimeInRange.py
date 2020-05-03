# return total number of prime Numbers in the range for a given number.
# x= 25 then total prime number in range of 25

def getPrimesCount(x):
    primes = [2]
    for i in range(3,x,2):
        for num in range(3,i):
        #for num in primes:
            if(i%num) == 0:
            #if(i%num) ==0
                break

        else:
            primes.append(i)

    print(primes)
    return(len(primes))

print(getPrimesCount(100))
