from collections import deque
class queue(deque):
  push = deque.append
  pop = deque.popleft
  def peek(self): return self[0]
  def is_empty(self): return len(self) == 0

struct bfs
{
  graph g;
  vector<int> p; // parents
  vector<int> d; // distances
  
  bfs(graph g) : g(g) {}

  void run(int s)
  {
    p.assign(g.n, -1); p[s] = s;
    d.assign(g.n, -1); d[s] = 0;
    queue<int> q; q.push(s);
    while(!q.empty())
    {
      int v = q.front(); q.pop();
      for (int u : g.adj[v])
      {
        if (p[u] != -1) continue;
        p[u] = v;
        d[u] = d[v]+1;
        q.push(u);
      }
    }
  }
};