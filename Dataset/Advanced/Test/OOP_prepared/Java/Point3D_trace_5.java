package Point3D;

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
        Point3D p1 = new Point3D();
        p1.setXYZ(13.4f, 14.5f, 15.6f);
        System.out.println(p1);
    }
}