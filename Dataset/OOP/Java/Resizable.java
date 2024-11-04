/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Resizable;

import GeometricObject.*;

/**
 *
 * @author GIA KINH
 */

public interface GeometricObject {
    public double getArea();
    public double getPerimeter();
}


public class Circle implements GeometricObject{

    protected double radius;

    public Circle(double radius) {
        this.radius = radius;
    }

    public Circle() {
    }

    public double getRadius() {
        return radius;
    }

    public void setRadius(double radius) {
        this.radius = radius;
    }

    @Override
    public String toString() {
        return "Circle[" + "radius=" + radius + ']';
    }
    
    
    
    @Override
    public double getArea() {
        return radius*radius*Math.PI;
    }

    @Override
    public double getPerimeter() {
        return radius*2*Math.PI;
    }
    
}

public interface Resizable {
    public abstract void resize(int percent);
}


public class ResizableCircle extends Circle implements Resizable{

    public ResizableCircle(double radius) {
        super(radius);
    }

    public ResizableCircle() {
    }

    @Override
    public String toString() {
        return "ResizableCircle[" + super.toString() +']';
    }

    
    
    @Override
    public void resize(int percent) {
        radius *= percent/100;
    }
    
}


public class TestMain {
    public static void main(String[] args) {
         GeometricObject g1 = new Circle(1.2);
        System.out.println(g1);
        System.out.println("Perimeter = "+g1.getPerimeter());
        System.out.println("Area = "+ g1.getArea());

        Resizable g2 = new ResizableCircle(3.4);
        System.out.println(g2);
        g2.resize(56);
        System.out.println(g2);
        

        GeometricObject g3 = (GeometricObject) g2;
        System.out.println(g3);
        System.out.println("Perimeter = "+g3.getPerimeter());
        System.out.println("Area = "+g3.getArea());
    }
}


