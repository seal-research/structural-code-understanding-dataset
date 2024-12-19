from datetime import datetime, timedelta
import logging

class MyDate:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def get_year(self):
        return self.year

    def set_year(self, year):
        self.year = year

    def get_month(self):
        return self.month

    def set_month(self, month):
        self.month = month

    def get_day(self):
        return self.day

    def set_day(self, day):
        self.day = day

    def __str__(self):
        date_string = f"{self.year}-{self.month}-{self.day}"
        try:
            date = datetime.strptime(date_string, "%Y-%m-%d")
        except ValueError as ex:
            logging.error("Error parsing date: %s", ex)
            return ""
        return date.strftime("%A %d %b %Y")

    def next_year(self):
        self.year += 1
        return self

    def next_month(self):
        self.month += 1
        return self

    def next_day(self):
        self.day += 1
        return self

    def previous_year(self):
        self.year -= 1
        return self

    def previous_month(self):
        self.month -= 1
        return self

    def previous_day(self):
        self.day -= 1
        return self

class TestMyDate:
    @staticmethod
    def is_leap_year(year):
        if year % 400 == 0:
            return True
        if year % 4 == 0 and year % 100 != 0:
            return True
        return False

    @staticmethod
    def is_valid_date(year, month, day):
        try:
            datetime(year, month, day)
        except ValueError:
            return False
        return True

    @staticmethod
    def get_day_of_week(year, month, day):
        weeks = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        try:
            date = datetime(year, month, day)
        except ValueError as ex:
            logging.error("Error parsing date: %s", ex)
            return -1
        day_of_week = date.strftime("%A")
        return weeks.index(day_of_week)

if __name__ == "__main__":
    d1 = MyDate(2012, 2, 28)
    print(d1)             # Tuesday 28 Feb 2012
    print(d1.next_day())  # Wednesday 29 Feb 2012
    print(d1.next_day())  # Thursday 1 Mar 2012
    print(d1.next_month())# Sunday 1 Apr 2012
    print(d1.next_year()) # Monday 1 Apr 2013

    d2 = MyDate(2012, 1, 2)
    print(d2)                 # Monday 2 Jan 2012
    print(d2.previous_day())  # Sunday 1 Jan 2012
    print(d2.previous_day())  # Saturday 31 Dec 2011
    print(d2.previous_month())# Wednesday 30 Nov 2011
    print(d2.previous_year()) # Tuesday 30 Nov 2010

    d3 = MyDate(2012, 2, 29)
    print(d3.previous_year()) # Monday 28 Feb 2011
    d4 = MyDate(2099, 11, 31) # Invalid year, month, or day!
    d5 = MyDate(2011, 2, 29)  # Invalid year, month, or day!
    print(d4)
    print(d5)
    print(TestMyDate.get_day_of_week(2099, 10, 31))
    print(TestMyDate.is_valid_date(2099, 10, 32))