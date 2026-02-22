from collections import deque
class queue(deque):
  push = deque.append
  pop = deque.popleft
  def peek(self): return self[0]
  def is_empty(self): return len(self) == 0
