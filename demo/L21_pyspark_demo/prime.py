import math

def is_prime(n):
    if n < 1: # Primse must be naturals.
        return False
    if n==1:
        return False
    for x in range(2,max([3,int(math.sqrt(n))])):
        if n%x==0:
            return False
    return True 
