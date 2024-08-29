# Create a program to validate the age of the voter with the help of custom exception. Voters whose age is less than 18 should not be allowed to vote.

class UnderageVoter(Exception):
    pass

def validate(age):
    try :
        if age<18:
            raise UnderageVoter("You are not allowed to vote. Age should be greater than 18")
        else:
            print("You are allowed to cast your vote")
    except UnderageVoter as e:
        print(e)
    finally:
        print("Thank you for coming!")
    

validate(17)

    