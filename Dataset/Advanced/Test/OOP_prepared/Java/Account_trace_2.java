public class Account {
    private String id;
    private String name;
    private int balance;

    public Account(String id, String name) {
        this.id = id;
        this.name = name;
    }

    public Account(String id, String name, int balance) {
        this.id = id;
        this.name = name;
        this.balance = balance;
    }

    public String getID() {
        return id;
    }

    public void setID(String id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getBalance() {
        return balance;
    }

    public void setBalance(int balance) {
        this.balance = balance;
    }
    
    public int credit(int amount){
        this.balance += amount;
        return this.balance;
    }
    
    public int debit(int amount){
        if(amount<=this.balance){
           this.balance-=amount;
        }else{
            System.out.println("Amount exceeded balance");
        }
        return this.balance;
    }
    
    public int transferTo(Account account, int amount){
        if(amount<=this.balance){
            account.balance += amount;
            this.balance -= amount;
        }else{
            System.out.println("Amount exceeded balance");
        }
        return this.balance;
    }

    @Override
    public String toString() {
        return "Account[" + "id=" + id + ",name=" + name + ",balance=" + balance + ']';
    }
  
}

class TestAccount {
   public static void main(String[] args) {
      Account a1 = new Account("A101", "Tan Ah Teck", 88);
      Account a2 = new Account("A102", "Kumar", 50);
      a1.transferTo(a2, 100);
   }
}