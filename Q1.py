from collections import Counter

class Arithematics(list):
    lst = []
    def __init__(self, lst):
        self.lst = lst
        self.len = len(lst)

    def mean(self):
        
        return sum(self.lst)/self.len
    
    def median(self):
        self.nlst = sorted(self.lst)
        print(self.lst)
        mid = self.len//2
        if self.len%2 == 1:
            return self.nlst[self.len//2] 
        else:
            return (self.nlst[mid - 1] + self.nlst[mid])/2

    def mode(self):        
        counts = Counter(self.lst)
        max_count = max(counts.values())        
        
        modes = [k for k, v in counts.items() if v == max_count]
        
        return modes


lst = [1,4,5,3,6,7,2,2,1,4]
s = Arithematics(lst)

print(s.mean())
print(s.median())
print(s.mode())