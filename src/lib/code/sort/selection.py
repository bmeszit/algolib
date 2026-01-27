def rendezes(T):
  n = len(T)
  for j in range(0, n-1):
    min_ertek = T[j]
    min_hely = j
    for i in range(j+1, n):
      if T[i] < min_ertek:
        min_ertek = T[i]
        min_hely = i
    T[j], T[min_hely] = T[min_hely], T[j]
  return T