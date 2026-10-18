// ======== COPIAR A LEETCODE DESDE AQUÍ ========
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
#ifdef LOCAL
#include "lc_local.hpp"  // TreeNode, ListNode y parsers de literales; en LeetCode ya existen
#endif

// LeetCode 226 - Invert Binary Tree
class Solution {
public:
    // Tiempo: O(n) | Memoria: O(h) de pila de recursión (h = altura)
    TreeNode* invertTree(TreeNode* root) {
        if (!root) return nullptr;
        swap(root->left, root->right);
        invertTree(root->left);
        invertTree(root->right);
        return root;
    }
};
// ======== HASTA AQUÍ ========

#ifdef LOCAL
int main() {
    string line;
    while (getline(cin, line)) cout << toString(Solution().invertTree(parseTree(line))) << el;
    return 0;
}
#endif
