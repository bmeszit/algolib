def rendezes(T):
  n = len(T)
  for j in range(n-1, 0, -1):
    for i in range(0, j):
      if T[i] > T[i+1]:
        T[i], T[i+1] = T[i+1], T[i]
  return T