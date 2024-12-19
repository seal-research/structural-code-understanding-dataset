class Author:
    def __init__(self, name=None, email=None, gender=None):
        self.name = name
        self.email = email
        if gender in ('m', 'f'):
            self.gender = gender
        else:
            print("Gender must be 'm' or 'f'")

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def get_gender(self):
        return self.gender

    def set_gender(self, gender):
        if gender in ('m', 'f'):
            self.gender = gender
        else:
            print("Gender must be 'm' or 'f'")

    def __str__(self):
        return f"Author[name={self.name}, email={self.email}, gender={self.gender}]"


class Book:
    def __init__(self, name, author, price, qty=0):
        self.name = name
        self.author = author
        self.price = price
        self.qty = qty

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

    def __str__(self):
        return f"Book[name={self.name}, {self.author}, price={self.price}, qty={self.qty}]"


if __name__ == "__main__":
    author3 = Author("Charlie Brown", "charlie.brown@example.com", 'm')
    book3 = Book("Data Structures", author3, 30.0, 0)
    book3.set_name("Algorithms and Data Structures")
    book3.set_price(35.0)
    print(book3)