class Customer:
    def __init__(self, id, name, discount):
        self._id = id
        self._name = name
        self._discount = discount

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_discount(self):
        return self._discount

    def set_discount(self, discount):
        self._discount = discount

    def __str__(self):
        return f"{self._name}({self._id})({self._discount}%)"


class Invoice:
    def __init__(self, id, customer, amount):
        self._id = id
        self._customer = customer
        self._amount = amount

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id

    def get_customer(self):
        return self._customer

    def set_customer(self, customer):
        self._customer = customer

    def get_amount(self):
        return self._amount

    def set_amount(self, amount):
        self._amount = amount

    def get_customer_id(self):
        return self._customer.get_id()

    def get_customer_name(self):
        return self._customer.get_name()

    def get_customer_discount(self):
        return self._customer.get_discount()

    def get_amount_after_discount(self):
        return self._amount - ((self._amount * self._customer.get_discount()) / 100)

    def __str__(self):
        return f"Invoice[id={self._id},customer={self._customer},amount={self._amount}]"


if __name__ == "__main__":
    c1 = Customer(88, "Tan Ah Teck", 10)
    print(c1)  # Customer's __str__()

    c1.set_discount(8)
    print(c1)
    print(f"id is: {c1.get_id()}")
    print(f"name is: {c1.get_name()}")
    print(f"discount is: {c1.get_discount()}")

    # Test Invoice class
    inv1 = Invoice(101, c1, 888.8)
    print(inv1)

    inv1.set_amount(999.9)
    print(inv1)
    print(f"id is: {inv1.get_id()}")
    print(f"customer is: {inv1.get_customer()}")  # Customer's __str__()
    print(f"amount is: {inv1.get_amount()}")
    print(f"customer's id is: {inv1.get_customer_id()}")
    print(f"customer's name is: {inv1.get_customer_name()}")
    print(f"customer's discount is: {inv1.get_customer_discount()}")
    print(f"amount after discount is: {inv1.get_amount_after_discount():.2f}")