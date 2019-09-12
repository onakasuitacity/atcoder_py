# https://juppy.hatenablog.com/entry/2019/05/02/%E8%9F%BB%E6%9C%AC_python_%E3%82%BB%E3%82%B0%E3%83%A1%E3%83%B3%E3%83%88%E6%9C%A8_%E7%AB%B6%E6%8A%80%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0_Atcoder
class SegTree(object):
    from operator import add
    def __init__(self,A,f=add,u=0):
        n=2**((len(A)-1).bit_length())
        N=2*n-1
        self.__num=n
        self.__len=N
        self.__seg=[u]*N
        self.__f=f
        self.__u=u
        # init
        for i in range(len(A)): # set
            self.tree[n+i-1]=A[i]
        for i in range(n-2,-1,-1): # built, iの子のnodeは2i+1,2i+2
            self.tree[i]=f(self.tree[2*i+1],self.tree[2*i+2])

    def __repr__(self):
        return str(self.tree)

    @property
    def func(self):
        return self.__f

    @property
    def tree(self):
        return self.__seg

    def update(k,w):
        "A[k]=w"
        k+=self.__num-1
        self.tree[k]=w
        while k+1: # k=0の処理が終わったら-1になってる
            k=(k-1)//2 # kの親のnodeは(k-1)//2
            self.tree[k]=self.func(self.tree[k*2+1],self.tree[k*2+2])

    def sum(self,p,q): # reduce(f,A[p:q])
        if q<=p: return self.__u
        p+=self.__num-1
        q+=self.__num-2
        res=self.__u
        while q-p>1:
            if p&1==0:
                res=self.func(res,self.tree[p])
            if q&1==1:
                res=self.func(res,self.tree[q])
                q-=1
            p=p//2
            q=(q-1)//2
        if p==q: res=self.func(res,self.tree[p])
        else: res=self.func(self.func(res,self.tree[p]),self.tree[q])
        return res


#%% Example
A=[5,3,7,9,6,4,1,2] # given sequence
N=len(A)
seg=SegTree(A)
print(seg) # [37, 24, 13, 8, 16, 10, 3, 5, 3, 7, 9, 6, 4, 1, 2]