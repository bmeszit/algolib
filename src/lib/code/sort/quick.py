def particional(T, eleje, vege):
  pivot_ertek = T[vege]
  pivot_hely = vege
  i = eleje
  for j in range(eleje, vege):
    if T[j] < pivot_ertek:
      T[i], T[j] = T[j], T[i]
      i = i+1
  T[i], T[pivot_hely] = T[pivot_hely], T[i]
  return i

def helyben_rendez(T, eleje, vege):
  if not eleje<vege:
    return
  
  pivot_hely = particional(T, eleje, vege)
  helyben_rendez(T, eleje, pivot_hely-1)
  helyben_rendez(T, pivot_hely+1, vege)

def rendezes(T):
  n = len(T)
  helyben_rendez(T, 0, n-1)
  return T