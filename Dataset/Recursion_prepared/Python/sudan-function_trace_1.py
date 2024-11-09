# Aamrun, 11th July 2022

def F(n,x,y):
  if n==0:
    return x + y
  elif y==0:
    return x
  else:
    return F(n - 1, F(n, x, y - 1), F(n, x, y - 1) + y)

print("F(2,2,2) = ", F(2,2,2))