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

T = list(map(int, input().split()))
MERES_KEZD()
eredmeny = rendezes(T.copy())
MERES_VEG()
print(eredmeny)