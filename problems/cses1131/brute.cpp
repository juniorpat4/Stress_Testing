#ifndef TEMPLATE_H
#define TEMPLATE_H

#include <bits/stdc++.h>

#define fi first
#define se second
#define forn(i,n) for(int i=0; i< (int)n; ++i)
#define for1(i,n) for(int i=1; i<= (int)n; ++i)
#define fore(i,l,r) for(int i=(int)l; i<= (int)r; ++i)
#define ford(i,n) for(int i=(int)(n) - 1; i>= 0; --i)
#define fored(i,l,r) for(int i=(int)r; i>= (int)l; --i)
#define pb push_back
#define el '\n'
#if defined(LOCAL) && !defined(NDEBUG)
#define dbg(x) cerr<< #x<< " " << x<<el
#else
#define dbg(x) ((void)0)
#endif
#define ri(n) scanf("%d",&n)
#define sz(v) int(v.size())
#define all(v) v.begin(),v.end()
using namespace std;
typedef long long ll;
typedef double ld;
typedef pair<int,int> ii;
typedef pair<ll,ll> pll;
typedef tuple<int, int, int> iii;
typedef vector<int> vi;
typedef vector<ii> vii;
typedef vector<ll> vll;
typedef vector<ld> vd;

const int inf = 1e9, nax = 1e5+200, mod = 1e9 + 7;
const ld pi = acos(-1);
const ld eps= 1e-9;
int dr[] = {1,-1,0, 0,1,-1,-1, 1};
int dc[] = {0, 0,1,-1,1, 1,-1,-1};

ostream& operator<<(ostream& os, const ii& pa) {
  return os << "("<< pa.fi << ", " << pa.se << ")";
}

#endif // TEMPLATE_H

// Fuerza bruta: BFS desde cada nodo y quedarse con la mayor distancia. Tiempo: O(n^2)
int main() {
    int n;
    cin >> n;
    vector<vi> adj(n + 1);
    forn(i, n - 1) {
        int a, b;
        cin >> a >> b;
        adj[a].pb(b);
        adj[b].pb(a);
    }

    int best = 0;
    for1(start, n) {
        vi dist(n + 1, -1);
        queue<int> q;
        dist[start] = 0;
        q.push(start);
        while (!q.empty()) {
            int node = q.front();
            q.pop();
            best = max(best, dist[node]);
            for (int next : adj[node])
                if (dist[next] == -1) {
                    dist[next] = dist[node] + 1;
                    q.push(next);
                }
        }
    }
    cout << best << el;
    return 0;
}
