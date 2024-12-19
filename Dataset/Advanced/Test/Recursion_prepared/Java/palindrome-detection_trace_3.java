public static boolean pali(String testMe){
	StringBuilder sb = new StringBuilder(testMe);
	return testMe.equals(sb.reverse().toString());
}

public static void main(String[] args) {
    System.out.println(pali("madam"));
}