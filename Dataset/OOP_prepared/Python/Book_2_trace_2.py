class Author:
    def __init__(self, name=None, email=None, gender=None):
        self.name = name
        self.email = email
        if gender in ['m', 'f']:
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
        if gender in ['m', 'f']:
            self.gender = gender
        else:
            print("Gender must be 'm' or 'f'")

    def __str__(self):
        return f"Author[name={self.name}, email={self.email}, gender={self.gender}]"


class Book:
    def __init__(self, name=None, authors=None, price=0.0, qty=0):
        self.name = name
        self.authors = authors if authors is not None else []
        self.price = price
        self.qty = qty

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_authors(self):
        return self.authors

    def set_authors(self, authors):
        self.authors = authors

    def get_price(self):
        return self.price

    def set_price(self, price):
        self.price = price

    def get_qty(self):
        return self.qty

    def set_qty(self, qty):
        self.qty = qty

    def get_author_names(self):
        return ','.join(author.get_name() for author in self.authors)

    def __str__(self):
        authors_str = ','.join(str(author) for author in self.authors)
        return f"Book[name={self.name}, author={{ {authors_str} }}, price={self.price}, qty={self.qty}]"


if __name__ == "__main__":
    author2 = Author("Jane Smith", "jane@example.com", 'f')
    book1 = Book("Python Basics", [author2], 59.99, 10)
    print(book1)
    print(book1.get_author_names())