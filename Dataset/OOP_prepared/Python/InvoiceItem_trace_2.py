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


if __name__ == "__main__":
    inv2 = InvoiceItem("A102", "Pencil", 200, 0.25)
    inv2.set_qty(250)
    print(inv2.get_qty())
    print(inv2.get_total())
    print(inv2)