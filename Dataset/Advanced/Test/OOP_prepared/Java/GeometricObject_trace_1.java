package GeometricObject;

public interface GeometricObject {
    public double getArea();
    public double getPerimeter();
}

public class Circle implements GeometricObject{

    private double radius;

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

public class Rectangle implements GeometricObject{
    private double width;
    private double length;

    public Rectangle() {
    }

    public Rectangle(double width, double length) {
        this.width = width;
        this.length = length;
    }

    public double getWidth() {
        return width;
    }

    public void setWidth(double width) {
        this.width = width;
    }

    public double getLength() {
        return length;
    }

    public void setLength(double length) {
        this.length = length;
    }

    @Override
    public String toString() {
        return "Rectangle[" + "width=" + width + ",length=" + length + ']';
    }

    @Override
    public double getArea() {
        return length*width;
    }

    @Override
    public double getPerimeter() {
        return (width+length)*2;
    }
}

public class TestMain {
    public static void main(String[] args) {
        GeometricObject c1 = new Circle(3.5);
        System.out.println("Area: " + c1.getArea());
    }
}