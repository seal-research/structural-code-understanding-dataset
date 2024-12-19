public class Rectangle {
    private float length;
    private float width;

    public Rectangle() {
        this.length = 1.0f;
        this.width = 1.0f;
    }

    public Rectangle(float length, float width) {
        this.length = length;
        this.width = width;
    }

    public float getLength() {
        return length;
    }

    public void setLength(float length) {
        this.length = length;
    }

    public float getWidth() {
        return width;
    }

    public void setWidth(float width) {
        this.width = width;
    }
    
    public float getArea(){
        return this.length * this.width;
    }
    
    public float getPerimeter(){
        return (this.length + this.width) * 2;
    }

    @Override
    public String toString() {
        return "Rectangle[" + "length=" + length + ", width=" + width + ']';
    }
}

class TestRectangle{
    public static void main(String[] args) {
        Rectangle r = new Rectangle(10.0f, 12.0f);
        System.out.printf("area is: %.2f%n", r.getArea());
    }
}