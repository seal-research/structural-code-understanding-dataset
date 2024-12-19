class Customer:
    def __init__(self, ID, name, discount=None, gender=None):
        self.ID = ID
        self.name = name
        self.discount = discount
        if gender in ['m', 'f']:
            self.gender = gender
        elif gender is not None:
            print("Gender must be 'm' or 'f'")

    def getID(self):
        return self.ID

    def setID(self, ID):
        self.ID = ID

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getGender(self):
        return self.gender

    def setGender(self, gender):
        if gender in ['m', 'f']:
            self.gender = gender
        else:
            print("Gender must be 'm' or 'f'")

    def getDiscount(self):
        return self.discount

    def setDiscount(self, discount):
        self.discount = discount

    def __str__(self):
        return f"{self.name}({self.ID})"


class Account:
    def __init__(self, id, customer, balance=0.0):
        self.id = id
        self.customer = customer
        self.balance = balance

    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id

    def getCustomer(self):
        return self.customer

    def setCustomer(self, customer):
        self.customer = customer

    def getBalance(self):
        return self.balance

    def setBalance(self, balance):
        self.balance = balance

    def getCustomerName(self):
        return self.customer.getName()

    def deposit(self, amount):
        self.balance += amount
        return self

    def withdraw(self, amount):
        if amount > self.balance:
            print("Amount withdraw exceeds the current balance!")
        else:
            self.balance -= amount
        return self

    def __str__(self):
        return f"{self.customer.getName()}({self.id}) balance=${self.balance:.2f}"


if __name__ == "__main__":
    customer1 = Customer(2, "Ha Gia Kinh", gender='m', discount=0.1)  # 10% discount
    customer2 = Customer(3, "Nguyen Thao", gender='f', discount=0.05)  # 5% discount
    customer3 = Customer(4, "Pham Tuong", gender='m', discount=0.2)  # 20% discount
    
    account1 = Account(1, customer1, 10000.0)
    account2 = Account(2, customer2, 5000.0)
    account3 = Account(3, customer3, 2000.0)
    
    # Perform transactions with discounts applied
    account1.withdraw(1000)
    account2.deposit(2000)
    account3.withdraw(2500)
    account2.deposit(1500)
    account3.withdraw(500)
    
    # Apply discounts to deposits and withdrawals
    account1.deposit(5000 * (1 - customer1.getDiscount()))  # Applying customer discount
    account2.withdraw(2000 * (1 - customer2.getDiscount()))  # Applying customer discount
    account3.deposit(3000 * (1 - customer3.getDiscount()))  # Applying customer discount