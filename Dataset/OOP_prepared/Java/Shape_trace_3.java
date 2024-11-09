package Shape;

/**
 *
 * @author GIA KINH
 */
public class Circle extends Shape{
    private double radius=1.0;

    public Circle() {
    }
    
    public Circle(double radius) {
        this.radius = radius;
    }

    public Circle(double radius, String color, boolean filled) {
        super(color, filled);
        this.radius = radius;
    }
    
    public double getArea(){
        return this.radius*this.radius*Math.PI;
    }
    
    public double getPerimeter(){
        return this.radius*2*Math.PI;
    }

    @Override
    public String toString() {
        return "Circle["+ super.toString() + ",radius=" + radius + ']';
    }

    public void setRadius(int radius) {
         this.radius = radius;//To change body of generated methods, choose Tools | Templates.
    }
}

package Shape;

/**
 *
 * @author GIA KINH
 */
public class Rectangle extends Shape{
    private double width;
    private double length;

    public Rectangle() {
    }

    public Rectangle(double width, double length) {
        this.width = width;
        this.length = length;
    }

    public Rectangle(double width, double length, String color, boolean filled) {
        super(color, filled);
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
    
    public double getArea(){
        return this.length*this.width;
    }
    
    public double getPerimeter(){
        return (this.length+this.width)*2;
    }

    @Override
    public String toString() {
        return "Rectangle["+ super.toString() + ",width=" + width + ", length=" + length + ']';
    }
}

package Shape;

/**
 *
 * @author GIA KINH
 */
public class Shape {
    private String color="red";
    private boolean filled=true;

    public Shape() {
    }

    public Shape(String color, boolean filled) {
        this.color = color;
        this.filled = filled;
    }

    public String getColor() {
        return color;
    }

    public void setColor(String color) {
        this.color = color;
    }

    public boolean isFilled() {
        return filled;
    }

    public void setFilled(boolean filled) {
        this.filled = filled;
    }

    @Override
    public String toString() {
        return "Shape[" + "color=" + color + ",filled=" + filled + ']';
    }
}

package Shape;

/**
 *
 * @author GIA KINH
 */
public class Square extends Rectangle{

    public Square() {
    }

    public Square(double side) {
        super(side, side);
    }

    public Square(double side, String color, boolean filled) {
        super(side, side, color, filled);
    }
    
    public double getSide(){
        return this.getLength();
    }
    
    public void setWidth(double side){
        super.setWidth(side);
        super.setLength(side);
    }
    
    public void setLength(double side){
        super.setWidth(side);
        super.setLength(side);
    }
    
    @Override
    public String toString(){
        return "Square["+super.toString()+"]";
    }
}

package Shape;

/**
 *
 * @author GIA KINH
 */
public class TestMain {

    public static void main(String[] args) {
        Circle c3 = new Circle(15);
        System.out.println("Area: " + c3.getArea());
    }
}