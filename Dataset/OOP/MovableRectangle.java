/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package MovableRectangle;

import MovableCircle.*;
import MovablePoint.*;

/**
 *
 * @author GIA KINH
 */
public interface Movable {
    public abstract void moveUp();
    public abstract void moveDown();
    public abstract void moveLeft();
    public abstract void moveRight();
}


public class MovablePoint implements Movable{
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
       this.y-=this.ySpeed;
    }

    @Override
    public void moveDown() {
        this.y+=this.ySpeed;
    }

    @Override
    public void moveLeft() {
        this.x-=this.xSpeed;
    }

    @Override
    public void moveRight() {
        this.x+=this.xSpeed;
    }
}


public class MovableRectangle implements Movable {

    private MovablePoint topLeft;
    private MovablePoint bottomRight;

    public MovableRectangle() {
    }

    public MovableRectangle(MovablePoint topLeft, MovablePoint bottomRight) {
        this.topLeft = topLeft;
        this.bottomRight = bottomRight;
    }

    public MovablePoint getTopLeft() {
        return topLeft;
    }

    public void setTopLeft(MovablePoint topLeft) {
        this.topLeft = topLeft;
    }

    public MovablePoint getBottomRight() {
        return bottomRight;
    }

    public void setBottomRight(MovablePoint bottomRight) {
        this.bottomRight = bottomRight;
    }

    @Override
    public String toString() {
        return "MovableRectangle[" + "topLeft=" + topLeft + ",bottomRight=" + bottomRight + ']';
    }

    @Override
    public void moveUp() {
        this.topLeft.setY(this.topLeft.getY() - this.topLeft.getySpeed());
        this.bottomRight.setY(this.bottomRight.getY() - this.bottomRight.getySpeed());
    }

    @Override
    public void moveDown() {
        this.topLeft.setY(this.topLeft.getY() + this.topLeft.getySpeed());
        this.bottomRight.setY(this.bottomRight.getY() + this.bottomRight.getySpeed());
    }

    @Override
    public void moveLeft() {
        this.topLeft.setX(this.topLeft.getX() - this.topLeft.getxSpeed());
        this.bottomRight.setX(this.bottomRight.getX() - this.bottomRight.getxSpeed());
    }

    @Override
    public void moveRight() {
        this.topLeft.setX(this.topLeft.getX() + this.topLeft.getxSpeed());
        this.bottomRight.setX(this.bottomRight.getX() + this.bottomRight.getxSpeed());
    }

}

public class TestMain {

    public static void main(String[] args) {
        
    }
}


