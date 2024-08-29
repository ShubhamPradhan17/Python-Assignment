# Create function to generate data randomly with python standard library

import random


def generaterandom(a,b):
    return random.randint(a,b) 


n = generaterandom(0,100)

print(n)