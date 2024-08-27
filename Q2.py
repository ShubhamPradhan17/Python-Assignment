a = ["ab" , "abc" , "aba"]


for i in a:
    if i == i[::-1]:
        print( i + " is a Palindrome")
    else:
        print(i + " not a Palindrome")

