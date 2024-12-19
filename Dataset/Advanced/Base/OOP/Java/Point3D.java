/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Point3D;

/**
 *
 * @author GIA KINH
 */
public class Point2D {
    private float x;
    private float y;

    public Point2D() {
    }

    public Point2D(float x, float y) {
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

public class Point3D extends Point2D{
    private float z;

    public Point3D() {
    }

    public Point3D(float x, float y, float z) {
        super(x, y);
        this.z = z;
    }

    public float getZ() {
        return z;
    }

    public void setZ(float z) {
        this.z = z;
    }
    
    public void setXYZ(float x, float y, float z){
        this.setXY(x, y);
        this.z=z;
    }
    
    public float[] getXYZ(){
        float[] list = new float[]{this.getX(),this.getY(),this.z};
        return list;
    }

    @Override
    public String toString() {
        return "(" + this.getX() + "," + this.getY() + "," + z + '}';
    }
}


class TestPoint3D {

    public static void main(String[] args) {
        Point3D p1 = new Point3D(1, 2, 3);
        System.out.println(p1);

        p1.setX(4);
        p1.setY(5);
        p1.setZ(6);
        System.out.println(p1);
        System.out.println("point X : " + p1.getX());
        System.out.println("point Y : " + p1.getY());
        System.out.println("point Z : " + p1.getZ());

        p1.setXY(7, 8);
        System.out.println(p1);
        p1.setXYZ(9, 10, 11);
        System.out.println("new point: " + Arrays.toString(p1.getXYZ()));

    }
}


