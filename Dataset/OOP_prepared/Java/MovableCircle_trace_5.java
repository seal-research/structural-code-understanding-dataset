public interface Movable {
    public abstract void moveUp();
    public abstract void moveDown();
    public abstract void moveLeft();
    public abstract void moveRight();
}

package MovableCircle;

public class MovableCircle implements Movable {
    private int radius;
    private MovablePoint center;

    public MovableCircle() {
    }

    public MovableCircle(int radius, MovablePoint center) {
        this.radius = radius;
        this.center = center;
    }
    
    public MovableCircle(int x, int y, int xSpeed, int ySpeed, int radius) {
        this.radius = radius;
        this.center = new MovablePoint(x, y, xSpeed, ySpeed);
    }

    public int getRadius() {
        return radius;
    }

    public void setRadius(int radius) {
        this.radius = radius;
    }

    public MovablePoint getCenter() {
        return center;
    }

    public void setCenter(MovablePoint center) {
        this.center = center;
    }

    @Override
    public String toString() {
        return center + ",radius=" + radius;
    }

    @Override
    public void moveUp() {
        this.center.setY(this.center.getY() - this.center.getySpeed());
    }

    @Override
    public void moveDown() {
        this.center.setY(this.center.getY() + this.center.getySpeed());
    }

    @Override
    public void moveLeft() {
        this.center.setX(this.center.getX() - this.center.getxSpeed());
    }

    @Override
    public void moveRight() {
        this.center.setX(this.center.getX() + this.center.getxSpeed());
    }
}

public class MovablePoint implements Movable {
    private int x;
    private int y;
    private int xSpeed;
    private int ySpeed;

    public MovablePoint() {
    }

    public MovablePoint(int x, int y, int xSpeed, int ySpeed) {
        this.x = x;
        this.y = y;
        this.xSpeed = xSpeed;
        this.ySpeed = ySpeed;
    }

    public int getX() {
        return x;
    }

    public void setX(int x) {
        this.x = x;
    }

    public int getY() {
        return y;
    }

    public void setY(int y) {
        this.y = y;
    }

    public int getxSpeed() {
        return xSpeed;
    }

    public void setxSpeed(int xSpeed) {
        this.xSpeed = xSpeed;
    }

    public int getySpeed() {
        return ySpeed;
    }

    public void setySpeed(int ySpeed) {
        this.ySpeed = ySpeed;
    }

    @Override
    public String toString() {
        return "(" + x + "," + y + ") speed=" + xSpeed + "," + ySpeed + ')';
    }

    @Override
    public void moveUp() {
        this.y -= this.ySpeed;
    }

    @Override
    public void moveDown() {
        this.y += this.ySpeed;
    }

    @Override
    public void moveLeft() {
        this.x -= this.xSpeed;
    }

    @Override
    public void moveRight() {
        this.x += this.xSpeed;
    }
}

public class TestMain {
    public static void main(String[] args) {
        Movable m1 = new MovablePoint(70, 80, 6, 6);
        System.out.println(m1);
        m1.moveUp();
        System.out.println(m1);
    }
}