package MyDate;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.Date;
import java.util.logging.Level;
import java.util.logging.Logger;

public class MyDate {

    private int year;
    private int month;
    private int day;

    public MyDate(int year, int month, int day) {
        this.year = year;
        this.month = month;
        this.day = day;
    }

    public int getYear() {
        return year;
    }

    public void setYear(int year) {
        this.year = year;
    }

    public int getMonth() {
        return month;
    }

    public void setMonth(int month) {
        this.month = month;
    }

    public int getDay() {
        return day;
    }

    public void setDay(int day) {
        this.day = day;
    }

    @Override
    public String toString() {
        String dateString = String.format("%d-%d-%d", year, month, day);
        Date date = null;
        try {
            date = new SimpleDateFormat("yyyy-MM-dd").parse(dateString);
        } catch (ParseException ex) {
            Logger.getLogger(MyDate.class.getName()).log(Level.SEVERE, null, ex);
        }
        dateString = new SimpleDateFormat("EEEE d MMM yyyy").format(date);
        return dateString;
    }

    public MyDate nextYear() {
        this.year++;
        return this;
    }

    public MyDate nextMonth() {
        this.month++;
        return this;
    }

    public MyDate nextDay() {
        this.day++;
        return this;
    }

    public MyDate previousYear() {
        this.year--;
        return this;
    }

    public MyDate previousMonth() {
        this.month--;
        return this;
    }

    public MyDate previousDay() {
        this.day--;
        return this;
    }
}

class TestMyDate {

    public static boolean isLeapYear(int year) {
        if(year % 400 == 0){
            return true; 
        }
        if (year % 4 == 0 && year % 100 != 0){
             return true;
        }
        return false;
    }

    public static boolean isValidDate(int year, int month, int day) {
        String dateString = String.format("%d-%d-%d", year, month, day);
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
        dateFormat.setLenient(false);
        try {
            dateFormat.parse(dateString);
        } catch (ParseException pe) {
            return false;
        }
        return true;
    }

    public static int getDayOfWeek(int year, int month, int day) {
        String[] weeks = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};

        String dateString = String.format("%d-%d-%d", year, month, day);
        Date date = null;
        try {
            date = new SimpleDateFormat("yyyy-MM-dd").parse(dateString);

        } catch (ParseException ex) {
            Logger.getLogger(MyDate.class
                    .getName()).log(Level.SEVERE, null, ex);
        }
        dateString = new SimpleDateFormat("EEEE").format(date);
        int d=0;
        for(String week: weeks){
            if(week.equals(dateString)) break;
            d++;
        }
        return d;
    }

    public static void main(String[] args) {
        System.out.println(isValidDate(2022, 2, 29));
    }
}