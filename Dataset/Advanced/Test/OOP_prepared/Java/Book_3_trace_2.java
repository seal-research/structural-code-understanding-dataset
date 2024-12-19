package Book3;

class Author {
    private String name;
    private String email;

    public Author(String name, String email) {
        this.name = name;
        this.email = email;
    }

    public Author() {
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    @Override
    public String toString() {
        return "Author[" + "name=" + name + ",email=" + email + ']';
    }
}

public class Book {
    private String isbn;
    private String name;
    private Author author;
    private Double price;
    private int qty;

    public Book(String isbn, String name, Author author, Double price) {
        this.isbn = isbn;
        this.name = name;
        this.author = author;
        this.price = price;
    }

    public Book(String isbn, String name, Author author, Double price, int qty) {
        this.isbn = isbn;
        this.name = name;
        this.author = author;
        this.price = price;
        this.qty = qty;
    }

    public String getIsbn() {
        return isbn;
    }

    public void setIsbn(String isbn) {
        this.isbn = isbn;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Author getAuthor() {
        return author;
    }

    public void setAuthor(Author author) {
        this.author = author;
    }

    public Double getPrice() {
        return price;
    }

    public void setPrice(Double price) {
        this.price = price;
    }

    public int getQty() {
        return qty;
    }

    public void setQty(int qty) {
        this.qty = qty;
    }
    
    public String getAuthorName(){
        return this.author.getName();
    }

    @Override
    public String toString() {
        return "Book[" + "isbn=" + isbn + ",name=" + name + "," + author + ",price=" + price + ",qty=" + qty + ']';
    } 
}

class TestBook {
    public static void main(String[] args) {
        Author a2 = new Author("Jane Smith", "jane@example.com");
        Book b2 = new Book("22222", "Advanced Java", a2, 25.0, 30);
        System.out.println(b2.getAuthorName());
    }
}