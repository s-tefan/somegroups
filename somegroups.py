import math


def powpow(a,n, identity):
    # power of monoid (semigroup) element to non-negative (positive) integer exponent
    # computed recursively
    if n >=2:
        q, r = divmod(n, 2)
        b = powpow(a, q, identity)
        if r:
            return b*b*a
        else:
            return b*b
    elif n == 1:
        return a
    else:
        return identity

class Group:
    pass

class GroupElement:
    def __init__(self, group):
        self.group = group

    def __mul__(self, other):
        return self.group.mul(self, other)
    
    def __pow__(self, n):
        return self.group.pow(self, n)

    def __str__(self):
        return(self.group.str(self))


class CyclicGroup(Group):

    def __init__(self, order):
        self.order = order


    def unit(self):
        e = GroupElement(self)
        e.order = self.order
        e.power = 0
        return e

    def generator(self):
        g = GroupElement(self)
        g.order = self.order
        g.power = 1
        return g

    def exp(self, n):
        g = GroupElement(self)
        g.power = n % self.order
        return g
    

    def mul(self, a, b):
        g = GroupElement(self)
        g.power = (a.power + b.power) % a.group.order
        return g
    
    def str(self, g):
        return(f'exp({g.power})')
    
    def pow(self, a, n):
        g = GroupElement(self)
        g.power = n*(a.power) % a.group.order
        return g
            

class DihedralGroup(Group):

    def __init__(self, halforder):
        self.halforder = halforder
        self.order = 2*halforder

    def unit(self):
        e = GroupElement(self)
        e.order = self.order
        e.power = 0
        e.reflektion = 0
        return e
    
    def mul(self, a, b):
        pass
    
    ### et c ...

class SymmetricGroup(Group):
    '''
    A symmetric group element is represented as a list of lists, each representing a cycle.
    Action of a groupelement on {0,...,n-1} as a permutation is composed from left to right. 
    '''

    def __init__(self, setorder):
        self.setorder = setorder # the group is acting on list(range(setorder))
        self.order = math.factorial(setorder)

    def unit(self):
        g = GroupElement(self)
        g.cyclelist = []
        return g
    
    def action_cyclelist(self, a, k):
        # a: list of not necessarily disjoint cycles, first goes first
        for c in a:
            if k in c:
                k = c[(c.index(k) + 1) % len(c)]
        return k
    
    def action_cyclelist_disj(self, a, k):
        # a: list of disjoint cycles, more effective
        for c in a:
            if k in c:
                return c[(c.index(k) + 1) % len(c)]
        return k
    
    def action(self, g, k):
        return self.action_cyclelist_disj(g.cyclelist, k)

    def disjoint_cyclelist(self, a):
        s = set(range(self.setorder))
        d = []
        while s:
            k = min(s)
            c = [k]
            s.remove(k)
            while True:
                k = self.action_cyclelist(a, c[-1])
                if k == c[0]:
                    break
                else:
                    c.append(k)
                    s.remove(k)
            if len(c) > 1:
                d.append(c)
        return d

    def from_cyclelist(self, cl):
        g = GroupElement(self)
        g.cyclelist = self.disjoint_cyclelist(cl)
        return g

    def mul(self, a, b):
        return self.from_cyclelist(a.cyclelist + b.cyclelist)

    def str(self, g):
        return str(g.cyclelist)
    
    def pow(self, g, n):
        return powpow(g, n, identity = self.unit())


C5 = CyclicGroup(5)
a = C5.unit()
b = C5.exp(3)
c = b*b
print(a.power, b.power, c.power, a.group, a.group.order)
for k in range(b.group.order):
    print (b.group.pow(b,k), b**k, (b**k).power)

S = SymmetricGroup(8)
sa = S.from_cyclelist([[0,1],[1,2,3],[3,4,5],[6,7]])
sb = S.from_cyclelist([[1,2,3],[3,4,5],[0,1],[6,7]])
for k in range(S.setorder):
    print(S.action(sa, k))

print(sa)
print(sb)

print(sa*sb)
print(sb*sa)
print(sa**2)
print(sa**3)
print(sa**4)
print(sa**5)
print(sa**6)


