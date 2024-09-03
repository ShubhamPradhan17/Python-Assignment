# Create a program to check eligibility of the person for loan  with the help of oops concepts and exception handling. Person whose salary is less than 10K/ Month will not be eligible for the loan.

class notEligible(Exception):
    pass

class Loan:
    def __init__(self, salary):
        self.salary = salary

    def checkEligibility(self):
        try:
            if self.salary < 10000: 
                raise notEligible("Sorry, You are not eligible for the loan.")
            else:
                print("You are eligible for the loan. Thank you.")
        except notEligible as e:
             print(e)


try:
    print("Please enter your monthly salary to check eligibility for loan - ")
    salary = int(input())
    person = Loan(salary)

except ValueError as e:
    print(e)

else:
    person.checkEligibility()