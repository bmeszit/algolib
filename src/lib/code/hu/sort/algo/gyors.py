def particional(T, eleje, vege):
  pivot_ertek = T[eleje]
  bal = eleje + 1
  jobb = vege
  
  while bal <= jobb:
    # Balról keresünk nagyobbat a pivotnál
    while bal <= jobb and T[bal] < pivot_ertek:
      bal += 1
    
    # Jobbról keresünk kisebbet a pivotnál
    while bal <= jobb and T[jobb] >= pivot_ertek:
      jobb -= 1
    
    # Ha találtunk cserélendő párt, cseréljük
    if bal < jobb:
      T[bal], T[jobb] = T[jobb], T[bal]
  
  # Pivotot a jobb mutató helyére cseréljük (ez lesz a végleges helye)
  T[eleje], T[jobb] = T[jobb], T[eleje]
  return jobb

def gyors_rendezes(T, eleje, vege):
  if not eleje<vege:
    return
  
  pivot_hely = particional(T, eleje, vege)
  gyors_rendezes(T, eleje, pivot_hely-1)
  gyors_rendezes(T, pivot_hely+1, vege)
  return T

T = list(map(int, input().split()))
n = len(T)
MERES_KEZD()
eredmeny = gyors_rendezes(T.copy(), 0, n-1)
MERES_VEG()
print(eredmeny)