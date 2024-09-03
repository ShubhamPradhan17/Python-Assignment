# [“name512”, “same1example”, “joy18full”] replace the digits from string inside list

lst = ['name512', 'same1example', 'joy18full']
count = 0   

for idx, ele in enumerate(lst):
    temp = ""
    for j in ele:
        if j.isalpha():
            temp += j
        else:
            continue
        
        lst[idx] = temp
print(lst)