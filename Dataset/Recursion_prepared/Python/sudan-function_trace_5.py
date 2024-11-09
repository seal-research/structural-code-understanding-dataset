# Aamrun, 11th July 2022

def F(n,x,y):
  if n==0:
    return x + y
  elif y==0:
    return x
  else:
    return F(n - 1, F(n, x, y - 1), F(n, x, y - 1) + y)

if __name__ == '__main__':
  print("F(1,3,4) = ", F(1,3,4))