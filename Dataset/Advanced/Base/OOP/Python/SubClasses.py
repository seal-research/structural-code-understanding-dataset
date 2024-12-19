class Person:
    def __init__(self, name=None, address=None):
        self._name = name
        self._address = address

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = address

    def __str__(self):
        return f"Person[name={self._name}, address={self._address}]"


class Staff(Person):
    def __init__(self, name, address, school, pay):
        super().__init__(name, address)
        self._school = school
        self._pay = pay

    @property
    def school(self):
        return self._school

    @school.setter
    def school(self, school):
        self._school = school

    @property
    def pay(self):
        return self._pay

    @pay.setter
    def pay(self, pay):
        self._pay = pay

    def __str__(self):
        return f"Staff[{super().__str__()} school={self._school}, pay={self._pay}]"


class Student(Person):
    def __init__(self, name, address, program, year, fee):
        super().__init__(name, address)
        self._program = program
        self._year = year
        self._fee = fee

    @property
    def program(self):
        return self._program

    @program.setter
    def program(self, program):
        self._program = program

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, year):
        self._year = year

    @property
    def fee(self):
        return self._fee

    @fee.setter
    def fee(self, fee):
        self._fee = fee

    def __str__(self):
        return f"Student[{super().__str__()}, program={self._program}, year={self._year}, fee={self._fee}]"


def main():
    s1 = Student("Ha Gia Kinh", "Ha Noi", "PRO192", 2021, 300)
    print(s1)
    s1.address = "Quang Binh"
    print(s1)
    s1.fee = 300
    s1.program = "MAD101"
    s1.year = 2022
    print(f"Name is {s1.name}")
    print(f"Address is {s1.address}")
    print(f"Fee is {s1.fee}")
    print(f"Program is {s1.program}")
    print(f"Year is {s1.year}")

    sf1 = Staff("Dieu Linh", "Viet Nam", "Ba Vi", 250)
    print(sf1)
    sf1.address = "Japan"
    print(sf1)
    sf1.pay = 300
    sf1.school = "Tokyo Universe"
    print(f"Name is {sf1.name}")
    print(f"Address is {sf1.address}")
    print(f"Pay is {sf1.pay}")
    print(f"School is {sf1.school}")


if __name__ == "__main__":
    main()