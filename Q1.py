# [“name512”, “same1example”, “joy18full”] replace the digits from string inside list

lst = ['name512', 'same1example', 'joy18full']
count = 0   
for i in lst:
    temp = ""
    for j in i:
        if j.isalpha():
            temp += j
        else: 
            continue
    
    lst[count] = temp
    count+=1

print(lst)