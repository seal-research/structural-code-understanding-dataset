from datetime import datetime, timedelta

class MyTime:
    def __init__(self, hour, minute, second):
        self.hour = hour
        self.minute = minute
        self.second = second

    def get_hour(self):
        return self.hour

    def set_hour(self, hour):
        self.hour = hour

    def get_minute(self):
        return self.minute

    def set_minute(self, minute):
        self.minute = minute

    def get_second(self):
        return self.second

    def set_second(self, second):
        self.second = second

    def set_time(self, hour, minute, second):
        self.hour = hour
        self.minute = minute
        self.second = second

    def __str__(self):
        time_string = f"{self.hour:02}:{self.minute:02}:{self.second:02}"
        try:
            time = datetime.strptime(time_string, "%H:%M:%S")
        except ValueError as ex:
            print(f"Error parsing time: {ex}")
            return ""
        return time.strftime("%H:%M:%S")

    def next_hour(self):
        self.hour = (self.hour + 1) % 24
        return self

    def next_minute(self):
        self.minute = (self.minute + 1) % 60
        if self.minute == 0:
            self.next_hour()
        return self

    def next_second(self):
        self.second = (self.second + 1) % 60
        if self.second == 0:
            self.next_minute()
        return self

    def previous_hour(self):
        self.hour = (self.hour - 1) % 24
        return self

    def previous_minute(self):
        self.minute = (self.minute - 1) % 60
        if self.minute == 59:
            self.previous_hour()
        return self

    def previous_second(self):
        self.second = (self.second - 1) % 60
        if self.second == 59:
            self.previous_minute()
        return self

class TestMyTime:
    @staticmethod
    def main():
        my_time = MyTime(1, 1, 1)
        print(my_time)
        my_time.next_second()
        print(my_time)

if __name__ == "__main__":
    TestMyTime.main()