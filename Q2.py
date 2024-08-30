# Create a Bank Account in class which includes customer balance, day wise transactions, can transfer money to different person account, interest given to him with a specific percentage

class BankAccount:
    def __init__(self, account_number, account_holder, balance=0.0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = balance
        self.transactions = []

    def deposit(self, amount, date):
        if amount > 0:
            self.balance += amount
            self.transactions.append((date, 'Deposit', amount))
            return True
        return False

    def withdraw(self, amount, date):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transactions.append((date, 'Withdraw', amount))
            return True
        return False

    def transfer(self, amount, recipient_account, date):
        if self.withdraw(amount, date):
            recipient_account.deposit(amount, date)
            self.transactions.append((date, 'Transfer to', recipient_account.account_number, amount))
            recipient_account.transactions.append((date, 'Transfer from', self.account_number, amount))
            return True
        return False

    def add_interest(self, interest_rate):
        if interest_rate > 0:
            interest = self.balance * (interest_rate / 100)
            self.balance += interest
            self.transactions.append(('Interest', interest_rate, interest))
            return interest
        return 0

    def get_balance(self):
        return self.balance

    def get_transactions(self):
        return self.transactions


acc1 = BankAccount("12345", "Alice", 1000)
acc2 = BankAccount("67890", "Bob", 500)

acc1.deposit(200, "2024-07-01")
acc1.withdraw(150, "2024-07-02")
acc1.transfer(300, acc2, "2024-07-03")
interest_added = acc1.add_interest(5)  # Adding 5% interest

print(f"Account 1 balance: {acc1.get_balance()}")
print(f"Interest added to Account 1: {interest_added}")
print(f"Account 1 transactions: {acc1.get_transactions()}")

print(f"Account 2 balance: {acc2.get_balance()}")
print(f"Account 2 transactions: {acc2.get_transactions()}")










































