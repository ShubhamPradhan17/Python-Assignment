# Create animal base class with attribute and related methods then create sub concrete subclass using animal eg of subclass: cow, horse, dog


class Animal():
    def __init__(self, name, age):
        self.name = name
        self.age = age
        

    def haveFourlegs(self):
        return True
    
    def aboutme(self):
        return f"I am a {self.name} and my age is {self.age}"
        
        



class Cow(Animal):
    def __init__(self, name, age):
        super().__init__(name, age)
    def Milk(self):
        print("Yes, it give milk")


    
class Horse(Animal):
    def __init__(self, name, age):
        super().__init__(name, age)
    


class Dog(Animal):
    def __init__(self, name, age):
        super().__init__(name, age)    
    def Barks(self):
        return True


cow = Cow("Cow", 10)
dog = Dog("dog", 5)
horse = Horse("Horse", 15)


print(cow.aboutme())
print(dog.aboutme())
print(horse.aboutme())