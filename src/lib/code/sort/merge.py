def osszefesul(A, B):
  k = len(A)
  l = len(B)
  C = [None]*(k+l)
  
  i=0
  j=0
  h=0
  
  while i<k and j<l:
    if A[i] < B[j]:
      C[h] = A[i]
      i = i+1
      h = h+1
    else:
      C[h] = B[j]
      j = j+1
      h = h+1
  
  if i==k:
    while j<l:
      C[h]=B[j]
      j=j+1
      h=h+1
  elif j==l:
    while i<k:
      C[h]=A[i]
      i=i+1
      h=h+1
  return C

def rendezes(T):
  n = len(T)
  
  if n>1:
    A = rendezes(T[0 : n//2])
    B = rendezes(T[n//2 : n])
    T = osszefesul(A, B)
  return T