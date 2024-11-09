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
    s1 = Student("Charlie Davis", "Phoenix", "PHY505", 2027, 900)
    print(s1)


if __name__ == "__main__":
    main()