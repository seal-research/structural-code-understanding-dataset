public class Circle {
    private double radius;

    public Circle() {
        radius = 1.0;
    }

    public Circle(double radius) {
        this.radius = radius;
    }

    public double getRadius() {
        return radius;
    }

    public void setRadius(double radius) {
        this.radius = radius;
    }
    
    public double getArea() {
      return radius*radius*Math.PI;
    }

    public double getCircumference(){
        return radius*2*Math.PI;
    }

    @Override
    public String toString() {
        return "Circle[" + "radius=" + radius + ']';
    }
}

class TestCircle{
    public static void main(String[] args) {
        Circle c = new Circle(3.5);
        System.out.printf("area is: %.2f%n", c.getArea());
    }
}