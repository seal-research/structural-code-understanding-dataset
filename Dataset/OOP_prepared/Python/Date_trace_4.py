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
        d1 = Date(1, 1, 2000)
        print(d1)

if __name__ == "__main__":
    TestDate.main()