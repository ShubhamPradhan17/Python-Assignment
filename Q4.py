def slicing(lst , lower_bound , upper_bound):
    print(lst[lower_bound:upper_bound+1])

def Palindrome(a):
    if a == a[::-1]:
        print(a + " is a Palindrome")
    else:
        print(a +" is not a Palindrome")


def NonRepeating(a):
    flag = False
    for i in a:
        if a.count(i)>1:
            flag = True
            break              

    if flag:
        print(a + " contains duplicate")
    else:
        print(a + " doesnt contains duplicate")



slicing([1,2,3,4,5,65,6,7], 2 , 6 )  #slicing(list, lower_bound, upper_bound)
Palindrome("abc")  #Palindrome(string)
NonRepeating("ab")  #NonRepeating(string)