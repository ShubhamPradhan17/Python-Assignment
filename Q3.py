# Build a counter generator

def counter():
    count = 1
    while True:
        yield count  
        count += 1

vals = counter()

for i in range(5):
     print(next(vals))