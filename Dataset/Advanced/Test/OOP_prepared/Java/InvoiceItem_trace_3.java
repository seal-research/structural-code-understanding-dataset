public class InvoiceItem {
    private String id;
    private String desc;
    private int qty;
    private double unitPrice;

    public InvoiceItem(String id, String desc, int qty, double unitPrice) {
        this.id = id;
        this.desc = desc;
        this.qty = qty;
        this.unitPrice = unitPrice;
    }

    public String getID() {
        return id;
    }

    public void setID(String id) {
        this.id = id;
    }

    public String getDesc() {
        return desc;
    }

    public void setDesc(String desc) {
        this.desc = desc;
    }

    public int getQty() {
        return qty;
    }

    public void setQty(int qty) {
        this.qty = qty;
    }

    public double getUnitPrice() {
        return unitPrice;
    }

    public void setUnitPrice(double unitPrice) {
        this.unitPrice = unitPrice;
    }
    
    public double getTotal(){
       return this.unitPrice * this.qty;
    }

    @Override
    public String toString() {
        return "InvoiceItem[" + "id=" + id + ",desc=" + desc + ",qty=" + qty + ",unitPrice=" + unitPrice + ']';
    }
}

class TestInvoiceItem {
   public static void main(String[] args) {
      InvoiceItem inv1 = new InvoiceItem("D404", "Marker", 150, 1.75);
      System.out.println("The total is: " + inv1.getTotal());
   }
}