a = ["aab" , "abc" , "def"]


for i in a:
    flag = False
    for  j in i:
        if i.count(j) > 1:
            flag = True
            break
        else:
            flag = False

    if flag:
        print("Count is greater than 1")
    else:
        print("Count is less than 1")
