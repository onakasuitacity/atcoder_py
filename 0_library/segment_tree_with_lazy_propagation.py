# lazy-propagation segment tree
# http://tsutaj.hatenablog.com/entry/2017/03/30/224339
# http://beet-aizu.hatenablog.com/entry/2017/12/01/225955
# http://sugarknri.hatenablog.com/entry/2018/04/16/123016
class LazySegmentTree(object):
    def __init__(self, A, dot, unit, compose, identity, act):
        # A : array of monoid (M, dot, unit)
        # (S, compose, identity) : sub monoid of End(M)
        # compose : (f, g) -> fg (f, g in S)
        # act : (f, x) -> f(x) (f in S, x in M)
        logn = (len(A) - 1).bit_length()
        n = 1 << logn
        tree = [unit] * (2 * n)
        for i, v in enumerate(A):
            tree[i + n] = v
        for i in range(n - 1, 0, -1):
            tree[i] = dot(tree[i << 1], tree[i << 1 | 1])
        self._n, self._logn, self._tree, self._lazy = n, logn, tree, [identity] * (2 * n)
        self._dot, self._unit, self._compose, self._identity, self._act = dot, unit, compose, identity, act

    def _ascend(self, i):
        tree, lazy, dot, act = self._tree, self._lazy, self._dot, self._act
        while i > 1:
            i >>= 1
            tree[i] = act(lazy[i], dot(tree[i << 1], tree[i << 1 | 1]))

    def _descend(self, i):
        tree, lazy, identity, compose, act = self._tree, self._lazy, self._identity, self._compose, self._act
        for k in range(self._logn, 0, -1):
            p = i >> k
            f = lazy[p]
            tree[p << 1], lazy[p << 1] = act(f, tree[p << 1]), compose(f, lazy[p << 1])
            tree[p << 1 | 1], lazy[p << 1 | 1] = act(f, tree[p << 1 | 1]), compose(f, lazy[p << 1 | 1])
            lazy[p] = identity

    # A[i] <- f(A[i]) for all i in [l, r)
    def range_act(self, l, r, f):
        l += self._n
        r += self._n
        # propagation isn't necessary if S is commutative
        self._descend(l)
        self._descend(r - 1)
        l0, r0 = l, r
        tree, lazy, act, compose = self._tree, self._lazy, self._act, self._compose
        while l < r:
            if l & 1:
                tree[l], lazy[l] = act(f, tree[l]), compose(f, lazy[l])
                l += 1
            if r & 1:
                r -= 1
                tree[r], lazy[r] = act(f, tree[r]), compose(f, lazy[r])
            l >>= 1
            r >>= 1
        self._ascend(l0)
        self._ascend(r0 - 1)

    # calculate product of A[l:r]
    def sum(self, l, r):
        l += self._n
        r += self._n
        self._descend(l)
        self._descend(r - 1)
        l_val = r_val = self._unit
        tree, dot = self._tree, self._dot
        while l < r:
            if l & 1:
                l_val = dot(l_val, tree[l])
                l += 1
            if r & 1:
                r -= 1
                r_val = dot(tree[r], r_val)
            l >>= 1
            r >>= 1
        return dot(l_val, r_val)
