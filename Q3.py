# Build a counter generator

def counter():
     yield 1
     yield 2
     yield 3
     yield 4
     yield 5

vals = counter()

# print(vals.__next__())
# print(vals.__next__())
# print(vals.__next__())
# print(vals.__next__())
# print(vals.__next__())

for i in vals:
     print(i)