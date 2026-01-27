def rendezes(T):
  n = len(T)
  for j in range(1, n):
    i = j
    while T[i-1] > T[i] and i > 0:
      T[i-1], T[i] = T[i], T[i-1]
      i = i-1
  return T