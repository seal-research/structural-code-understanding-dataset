/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package MovablePoint;

/**
 *
 * @author GIA KINH
 */
public class Point {
    private float x;
    private float y;

    public Point() {
    }

    public Point(float x, float y) {
        this.x = x;
        this.y = y;
    }

    public float getX() {
        return x;
    }

    public void setX(float x) {
        this.x = x;
    }

    public float getY() {
        return y;
    }

    public void setY(float y) {
        this.y = y;
    }
    
    public void setXY(float x, float y){
        this.x = x;
        this.y = y;
    }
    
    public float[] getXY(){
        return new float[]{this.x,this.y};
    }

    @Override
    public String toString() {
        return "(" + x + "," + y + ')';
    }
}


public class MovablePoint extends Point{
    private float xSpeed;   
    private float ySpeed;
    
    public MovablePoint() {
    
    }

    public MovablePoint(float xSpeed, float ySpeed) {
        this.xSpeed = xSpeed;
        this.ySpeed = ySpeed;
    }

    public MovablePoint(float x, float y, float xSpeed, float ySpeed) {
        super(x, y);
        this.xSpeed = xSpeed;
        this.ySpeed = ySpeed;
    }

    public float getxSpeed() {
        return xSpeed;
    }

    public void setxSpeed(float xSpeed) {
        this.xSpeed = xSpeed;
    }

    public float getySpeed() {
        return ySpeed;
    }

    public void setySpeed(float ySpeed) {
        this.ySpeed = ySpeed;
    }
    
    public void setSpeed(float xSpeed, float ySpeed){
        this.xSpeed = xSpeed;
        this.ySpeed = ySpeed;
    }
    
    public float[] getSpeed(){
        return new float[]{xSpeed, ySpeed};
    }

    @Override
    public String toString() {
        return super.toString() + ",speed=" +"("+xSpeed+","+ySpeed+")";
    }
    
    public MovablePoint move(){
        this.setX(this.getX()+this.xSpeed);
        this.setY(this.getY()+this.ySpeed);
        return this;
    }
    
}

public class TestMovablePoint{
    public static void main(String[] args) {
        MovablePoint m1 = new MovablePoint();
        System.out.println(m1);
        MovablePoint m2 = new MovablePoint(1, 2);
        System.out.println(m2);
        MovablePoint m3 = new MovablePoint(3, 4, 5, 6);
        System.out.println(m3);
        
        m1.setX(7);
        m1.setY(8);
        m1.setxSpeed(9);
        m1.setySpeed(10);
        System.out.println(m1);
        System.out.println("Move: " + m1.move());
    }
}


