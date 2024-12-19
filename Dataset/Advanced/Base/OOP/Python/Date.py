from datetime import datetime

class Date:
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

    def get_day(self):
        return self.day

    def set_day(self, day):
        self.day = day

    def get_month(self):
        return self.month

    def set_month(self, month):
        self.month = month

    def get_year(self):
        return self.year

    def set_year(self, year):
        self.year = year

    def set_date(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

    def __str__(self):
        date_string = f"{self.year}-{self.month}-{self.day}"
        try:
            date = datetime.strptime(date_string, "%Y-%m-%d")
        except ValueError as ex:
            print(f"Error parsing date: {ex}")
            return ""
        
        new_string = date.strftime("%d/%m/%Y")
        return new_string


class TestDate:
    @staticmethod
    def main():
        # Test constructor and toString()
        d1 = Date(1, 2, 2014)
        print(d1)  # toString()

        # Test Setters and Getters
        d1.set_month(12)
        d1.set_day(9)
        d1.set_year(2099)
        print(d1)  # toString()
        print("Month:", d1.get_month())
        print("Day:", d1.get_day())
        print("Year:", d1.get_year())

        # Test setDate()
        d1.set_date(3, 4, 2016)
        print(d1)  # toString()


if __name__ == "__main__":
    TestDate.main()