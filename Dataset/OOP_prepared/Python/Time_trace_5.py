from datetime import datetime, timedelta

class Time:
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

    def next_second(self):
        self.second += 1
        if self.second >= 60:
            self.second = 0
            self.minute += 1
            if self.minute >= 60:
                self.minute = 0
                self.hour += 1
                if self.hour >= 24:
                    self.hour = 0
        return self

    def previous_second(self):
        self.second -= 1
        if self.second < 0:
            self.second = 59
            self.minute -= 1
            if self.minute < 0:
                self.minute = 59
                self.hour -= 1
                if self.hour < 0:
                    self.hour = 23
        return self

    def __str__(self):
        time_string = f"{self.hour:02}:{self.minute:02}:{self.second:02}"
        try:
            time = datetime.strptime(time_string, "%H:%M:%S")
        except ValueError as ex:
            print(f"Error parsing time: {ex}")
            return ""
        return time.strftime("%H:%M:%S")


if __name__ == "__main__":
    t5 = Time(7, 15, 30)
    t5.set_time(10, 30, 45)
    print(t5.next_second())