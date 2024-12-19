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


# Expanded test cases
if __name__ == "__main__":
    # Create two accounts
    a1 = Account("A101", "Tan Ah Teck", 88)
    a2 = Account("A102", "Kumar", 50)

    # Test credit method
    a1.credit(20)

    # Test debit method within balance
    a1.debit(30)

    # Test debit method exceeding balance
    a1.debit(100)  # Expected output: Amount exceeded balance

    # Test transfer_to method within balance
    a1.transfer_to(a2, 10)

    # Test transfer_to method exceeding balance
    a1.transfer_to(a2, 100)  # Expected output: Amount exceeded balance

    # Test setting and getting account ID
    a1.set_id("A105")
    a1.get_id()

    # Test setting and getting account name
    a1.set_name("John Doe")
    a1.get_name()

    # Test setting and getting balance
    a1.set_balance(200)
    a1.get_balance() 
