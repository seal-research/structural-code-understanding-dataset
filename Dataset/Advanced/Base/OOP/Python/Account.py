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


class TestAccount:
    @staticmethod
    def main():
        # Test constructor and __str__()
        a1 = Account("A101", "Tan Ah Teck", 88)
        print(a1)  # __str__()
        a2 = Account("A102", "Kumar")  # default balance
        print(a2)

        # Test Getters
        print("ID:", a1.get_id())
        print("Name:", a1.get_name())
        print("Balance:", a1.get_balance())

        # Test credit() and debit()
        a1.credit(100)
        print(a1)
        a1.debit(50)
        print(a1)
        a1.debit(500)  # debit() error
        print(a1)

        # Test transfer()
        a1.transfer_to(a2, 100)  # __str__()
        print(a1)
        print(a2)


if __name__ == "__main__":
    TestAccount.main()