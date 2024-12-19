class InvoiceItem:
    def __init__(self, id, desc, qty, unit_price):
        self.id = id
        self.desc = desc
        self.qty = qty
        self.unit_price = unit_price

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_desc(self):
        return self.desc

    def set_desc(self, desc):
        self.desc = desc

    def get_qty(self):
        return self.qty

    def set_qty(self, qty):
        self.qty = qty

    def get_unit_price(self):
        return self.unit_price

    def set_unit_price(self, unit_price):
        self.unit_price = unit_price

    def get_total(self):
        return self.unit_price * self.qty

    def __str__(self):
        return f"InvoiceItem[id={self.id}, desc={self.desc}, qty={self.qty}, unit_price={self.unit_price}]"


# Test the InvoiceItem class
if __name__ == "__main__":
    # Test constructor and __str__()
    inv1 = InvoiceItem("A101", "Pen Red", 888, 0.08)
    print(inv1)  # __str__()

    # Test Setters and Getters
    inv1.set_qty(999)
    inv1.set_unit_price(0.99)
    print(inv1)  # __str__()
    print("id is:", inv1.get_id())
    print("desc is:", inv1.get_desc())
    print("qty is:", inv1.get_qty())
    print("unit_price is:", inv1.get_unit_price())

    # Test get_total()
    print("The total is:", inv1.get_total())