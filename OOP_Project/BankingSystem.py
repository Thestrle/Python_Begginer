class BankAccount():
    #Class variable can be delaced here directly
    #account_type = "Savings"

    def __init__(self,owner,balance):
        self.owner = owner
        self.balance = balance

    def __str__(self):
        return f'{self.owner},{self.balance}'

    def deposit(self,money):
        self.balance = self.balance + money
        return f'Deposit completed New balance is {self.balance}'

    def withdraw(self,money):
        if money < self.balance:
            #return self.balance - money
            return "Withdraw accepted"
        else:
            return "Not enough fund available"


acc1 = BankAccount("Alok",500)
out1 = acc1.deposit(500)
print(out1)
out2 = acc1.withdraw(800)
print(out2)
