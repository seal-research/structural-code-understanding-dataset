class Author:
    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def __str__(self):
        return f"Author[name={self.name},email={self.email}]"


class Book:
    def __init__(self, isbn, name, author, price, qty=0):
        self.isbn = isbn
        self.name = name
        self.author = author
        self.price = price
        self.qty = qty

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, isbn):
        self.isbn = isbn

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_author(self):
        return self.author

    def set_author(self, author):
        self.author = author

    def get_price(self):
        return self.price

    def set_price(self, price):
        self.price = price

    def get_qty(self):
        return self.qty

    def set_qty(self, qty):
        self.qty = qty

    def get_author_name(self):
        return self.author.get_name()

    def __str__(self):
        return f"Book[isbn={self.isbn},name={self.name},{self.author},price={self.price},qty={self.qty}]"


if __name__ == "__main__":
    a1 = Author("Tan Ah Teck", "ahteck@nowhere.com")
    b1 = Book("12345", "Java for dummies", a1, 8.8, 88)
    b1.set_price(20.0)
    print(b1)