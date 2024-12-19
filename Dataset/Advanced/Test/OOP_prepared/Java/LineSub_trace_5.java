public class Point {

    private int x;
    private int y;

    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public String toString() {
        return "Point:(" + x + "," + y + ")";
    }

    public int getX() {
        return x;
    }

    public int getY() {
        return y;
    }

    public void setX(int x) {
        this.x = x;
    }

    public void setY(int y) {
        this.y = y;
    }

    public void setXY(int x, int y) {
        this.x = x;
        this.y = y;
    }
   
}

public class LineSub extends Point {
    
    private Point end;
    
    public LineSub(Point begin, Point end) {
        super(begin.getX(), begin.getY());
        this.end = end;
    }
    
    public LineSub(int beginX, int beginY, int endX, int endY) {
        super(beginX, beginY);
        this.end = new Point(endX, endY);
    }
    
    @Override
    public String toString() {
        return "LineSub[" + "begin=" + super.toString() + ",end=" + end + ']';
    }
    
    public Point getBegin() {
        return new Point(super.getX(), super.getY());
    }

    public Point getEnd() {        
        return this.end;
    }

    public void setBegin(int beginX, int beginY) {
        setXY(beginX, beginY);        
    }

    public void setEnd(int endX, int endY) {        
        this.end.setXY(endX, endY);
    }
    
    public int getBeginX() {
        return getX();
    }

    public int getBeginY() {        
        return getY();
    }

    public int getEndX() {        
        return this.end.getX();
    }

    public int getEndY() {        
        return this.end.getY();
    }
    
    public void setBeginX(int beginX) {        
        setX(beginX);
    }

    public void setBeginY(int beginY) {
        setY(beginY);
    }

    public void setBeginXY(int beginX, int beginY) {        
        setXY(beginX, beginY);
    }

    public void setEndX(int endX) {        
        this.end.setX(endX);
    }

    public void setEndY(int endY) {
        this.end.setY(endY);
    }

    public void setEndXY(int endX, int endY) {
        this.end.setXY(endX, endY);
    } 
    
    public int getLength() { 
        return (int)(Math.sqrt(Math.pow(this.end.getX()-super.getX(), 2)+ Math.pow(this.end.getY()-super.getY(), 2)));
    }

    public double getGradient() { 
       return (double)(Math.atan2(this.end.getY()-super.getY(), this.end.getX()-super.getX()));
   }
    
}

class TestLineSub {
    public static void main(String[] args) {
        LineSub lineSub = new LineSub(7, 1, 4, 5);
        System.out.println(lineSub.getLength());
    }
}