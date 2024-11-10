class Account:
    def __init__(self, id, name, balance=0):
        self.id = id
        self.name = name
        self.balance = balance

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_balance(self):
        return self.balance

    def set_balance(self, balance):
        self.balance = balance

    def credit(self, amount):
        self.balance += amount
        return self.balance

    def debit(self, amount):
        if amount <= self.balance:
            self.balance -= amount
        else:
            print("Amount exceeded balance")
        return self.balance

    def transfer_to(self, account, amount):
        if amount <= self.balance:
            account.balance += amount
            self.balance -= amount
        else:
            print("Amount exceeded balance")
        return self.balance

    def __str__(self):
        return f"Account[id={self.id},name={self.name},balance={self.balance}]"

if __name__ == "__main__":
     # Create accounts
    a1 = Account("A101", "Tan Ah Teck", 88)
    a2 = Account("A102", "Kumar", 50)
    a3 = Account("A103", "Rajesh", 1000)

    # Credit money to accounts
    a1.credit(200)  # Tan Ah Teck credits 200
    a2.credit(150)  # Kumar credits 150
    a3.credit(500)  # Rajesh credits 500

    # Debit money from accounts
    a1.debit(100)  # Tan Ah Teck withdraws 100
    a2.debit(75)  # Kumar withdraws 75
    a3.debit(300)  # Rajesh withdraws 300

    # Perform a failed debit operation
    a2.debit(200)  # Kumar tries to withdraw more than his balance, should show an error

    # Print out the final states of the accounts