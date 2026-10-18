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

// Codeforces 600B - Queries about less or equal elements
// Tiempo: O((n + m) log n) | Memoria: O(n)
void solve() {
    int n, m;
    cin >> n >> m;
    vi a(n);
    forn(i, n) cin >> a[i];
    sort(all(a));

    forn(j, m) {
        int b;
        cin >> b;
        // upper_bound apunta al primer elemento > b: su índice es la cantidad de elementos <= b
        cout << upper_bound(all(a), b) - a.begin() << " \n"[j == m - 1];
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    solve();  // un único caso: no se lee t
    return 0;
}
