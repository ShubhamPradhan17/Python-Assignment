# [1, “a”, 2, “b”, 3, “c”] filter digits and alphabets separately using inbuilt functions like map, filter or reduce

lst = [1, 'a', 2, 'b', 3, 'c']
       
    
s = filter(lambda x :  type(x)==str, lst)
print(list(s))

Integer = filter(lambda x :  type(x)==int, lst)
print(list(Integer))

