/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Subclasses;

/**
 *
 * @author GIA KINH
 */
public class Person {
    private String name;
    private String address;

    public Person() {
    }

    public Person(String name, String address) {
        this.name = name;
        this.address = address;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    @Override
    public String toString() {
        return "Person[" + "name=" + name + ",address=" + address + ']';
    }
}


public class Staff extends Person{
    private String school;
    private double pay;

    public Staff(String name, String address, String school, double pay) {
        super(name, address);
        this.school = school;
        this.pay = pay;
    }

    public String getSchool() {
        return school;
    }

    public void setSchool(String school) {
        this.school = school;
    }

    public double getPay() {
        return pay;
    }

    public void setPay(double pay) {
        this.pay = pay;
    }

    @Override
    public String toString() {
        return "Staff[" + super.toString() + "school=" + school + ", pay=" + pay + ']';
    }
    
    
}


public class Student extends Person{
    private String program;
    private int year;
    private double fee;

    public Student(String name, String address, String program, int year, double fee) {
        super(name, address);
        this.program = program;
        this.year = year;
        this.fee = fee;
    }
    
    public Student(String program, int year, double fee, String name, String address) {
        super(name, address);
        this.program = program;
        this.year = year;
        this.fee = fee;
    }


    public String getProgram() {
        return program;
    }

    public void setProgram(String program) {
        this.program = program;
    }

    public int getYear() {
        return year;
    }

    public void setYear(int year) {
        this.year = year;
    }

    public double getFee() {
        return fee;
    }

    public void setFee(double fee) {
        this.fee = fee;
    }

    @Override
    public String toString() {
        return "Student[" + super.toString() + ",program=" + program + ",year=" + year + ",fee=" + fee + ']';
    }
}


public class TestMain {

    public static void main(String[] args) {
        Student s1 = new Student("PRO192", 2021, 300, "Ha Gia Kinh", "Ha Noi");
        System.out.println(s1);
        s1.setAddress("Quang Binh");
        System.out.println(s1);
        s1.setFee(300);
        s1.setProgram("MAD101");
        s1.setYear(2022);
        System.out.println("Name is " + s1.getName());
        System.out.println("Adress is " + s1.getAddress());
        System.out.println("Fee is " + s1.getFee());
        System.out.println("Program is " + s1.getProgram());
        System.out.println("Year is " + s1.getYear());
        
        Staff sf1 = new Staff("Dieu Linh", "Viet Nam", "Ba Vi", 250);
        System.out.println(sf1);

        sf1.setAddress("Japan");
        System.out.println(sf1);
        sf1.setPay(300);
        sf1.setSchool("Tokyo Universe");
        System.out.println("Name is " + sf1.getName());
        System.out.println("Adress is " + sf1.getAddress());
        System.out.println("Pay is " + sf1.getPay());
        System.out.println("School is " + sf1.getSchool());
    }
}


