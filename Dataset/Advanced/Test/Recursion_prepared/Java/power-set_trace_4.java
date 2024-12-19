public static ArrayList<String> getpowerset(int a[], int n, ArrayList<String> ps) {
    if (n < 0) {
        return null;
    }
    if (n == 0) {
        if (ps == null)
            ps = new ArrayList<String>();
        ps.add(" ");
        return ps;
    }
    ps = getpowerset(a, n - 1, ps);
    ArrayList<String> tmp = new ArrayList<String>();
    for (String s : ps) {
        if (s.equals(" "))
            tmp.add("" + a[n - 1]);
        else
            tmp.add(s + a[n - 1]);
    }
    ps.addAll(tmp);
    return ps;
}

public static void main(String[] args) {
    int[] a = {11, 12, 13, 14, 15};
    ArrayList<String> ps = getpowerset(a, a.length, null);
    System.out.println(ps);
}