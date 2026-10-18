// Solo local: LeetCode ya define TreeNode y ListNode. Se incluye DESPUÉS de la plantilla
// (necesita <bits/stdc++.h> y using namespace std) y dentro de #ifdef LOCAL.
// Convierte literales LeetCode ("[1,null,2]") en estructuras y de vuelta.
#pragma once

struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x = 0, ListNode *nxt = nullptr) : val(x), next(nxt) {}
};

struct TreeNode {
    int val;
    TreeNode *left, *right;
    TreeNode(int x = 0, TreeNode *l = nullptr, TreeNode *r = nullptr) : val(x), left(l), right(r) {}
};

// "[1,null,2]" -> {1, nullopt, 2}
inline vector<optional<int>> lcTokens(string line) {
    for (char &c : line)
        if (c == '[' || c == ']' || c == ',') c = ' ';
    stringstream ss(line);
    vector<optional<int>> tokens;
    for (string tok; ss >> tok;) tokens.push_back(tok == "null" ? nullopt : optional<int>(stoi(tok)));
    return tokens;
}

inline vector<int> parseIntVector(const string& line) {
    vector<int> v;
    for (auto &tok : lcTokens(line)) v.push_back(tok.value());
    return v;
}

inline ListNode* parseList(const string& line) {
    ListNode dummy;
    ListNode *tail = &dummy;
    for (auto &tok : lcTokens(line)) tail = tail->next = new ListNode(tok.value());
    return dummy.next;
}

// Orden por niveles de LeetCode: cada nodo no nulo consume dos tokens (izquierdo, derecho).
inline TreeNode* parseTree(const string& line) {
    vector<optional<int>> tokens = lcTokens(line);
    if (tokens.empty() || !tokens[0]) return nullptr;
    TreeNode *root = new TreeNode(*tokens[0]);
    queue<TreeNode*> pending;
    pending.push(root);
    size_t i = 1;
    while (!pending.empty() && i < tokens.size()) {
        TreeNode *node = pending.front();
        pending.pop();
        for (TreeNode **child : {&node->left, &node->right}) {
            if (i < tokens.size() && tokens[i]) {
                *child = new TreeNode(*tokens[i]);
                pending.push(*child);
            }
            i++;
        }
    }
    return root;
}

inline string toString(const vector<optional<int>>& values) {
    string out = "[";
    for (size_t i = 0; i < values.size(); i++)
        out += (i ? "," : "") + (values[i] ? to_string(*values[i]) : string("null"));
    return out + "]";
}

inline string toString(const vector<int>& v) { return toString(vector<optional<int>>(v.begin(), v.end())); }

inline string toString(ListNode *head) {
    vector<optional<int>> values;
    for (; head; head = head->next) values.push_back(head->val);
    return toString(values);
}

inline string toString(TreeNode *root) {
    vector<optional<int>> values;
    queue<TreeNode*> q;
    q.push(root);
    while (!q.empty()) {
        TreeNode *node = q.front();
        q.pop();
        if (!node) {
            values.push_back(nullopt);
            continue;
        }
        values.push_back(node->val);
        q.push(node->left);
        q.push(node->right);
    }
    while (!values.empty() && !values.back()) values.pop_back();  // LeetCode omite los null finales
    return toString(values);
}
