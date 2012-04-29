#! /usr/bin/python
import sys
import math

class expr(object):
    _left = 0
    _right = 0
    _content = 0
    _phr=0
    def __init__(self,l,r):
        self._left = l
        self._right = r

    def differention(self):
        pass

    def evaluate(self):
        pass

    def set_priority(self):
        self._phr=1

    def get_node(self):
        if self._phr==1: 
            return '('+self._left.get_node()+self._content+self._right.get_node()+')'
        else:
            return self._left.get_node()+self._content+self._right.get_node()

    def _simplify(self,l,r):
        pass

    def simplify(self):
        r = self._right.simplify()
        l = self._left.simplify()
        if isinstance(r,value_expr) and isinstance(l,value_expr):
            return value_expr(self.evaluate())
        else:
            return self._simplify(l,r)

    def containx(self):
        return self._left.containx() or self._right.containx()

    def __eq__(self,a):
        if self._content == a._content:
            return self._left == a._left and self._right == a._right
        else:
            return False

class add_expr(expr):
    _content = '+' 
    def differention(self):
        return add_expr(self._left.differention(),self._right.differention())
    
    def evaluate(self):
        return self._left.evaluate()+self._right.evaluate()

    def _simplify(self,l,r):
        if isinstance(l,value_expr) and l._content==0:
            return r
        elif isinstance(r,value_expr) and r._content==0:
            return l
        else:
            self._right=r
            self._left=l
            return self

class sub_expr(expr):
    _content = '-'
    def differention(self):
        return sub_expr(self._left.differention(),self._right.differention())

    def evaluate(self):
        return self._left.evaluate()-self._right.evaluate()

    def _simplify(self,l,r):
        if  isinstance(l,value_expr) and l._content==0:
            return mul_expr(value_expr(-1),r)
        elif  isinstance(r,value_expr) and r._content==0:
            return l
        else:
            self._right=r
            self._left=l
            return self
    

class mul_expr(expr):
    _content = '*'
    def differention(self):
        return add_expr(mul_expr(self._left.differention(),self._right),mul_expr(self._left,self._right.differention()))
    
    def evaluate(self):
        return self._left.evaluate()*self._right.evaluate()

    def _simplify(self,l,r):
        if  ( isinstance(l,value_expr) and l._content==0) or ( isinstance(r,value_expr) and r._content==0):
            return value_expr(0)
        elif isinstance(l,value_expr) and l._content==1:
            return r
        elif isinstance(r,value_expr) and  r._content==1:
            return l
        else:
            self._right=r
            self._left=l
            return self

 


class div_expr(expr):
    _content = '/'
    def differention(self):
        return div_expr(add_expr(mul_expr(self._left.differention(),self._right),mul_expr(self._left,self._right.differention())),self._right)

    def evaluate(self):
        return self._left.evaluate()/self._right.evaluate()

    def _simplify(self,l,r):
        if  l._content==0:
            return value_expr(0)
        elif  r._content==0:
            raise Exception("Error:the value can't divided by 0")
        elif r._content==1:
            return l
        else:
            self._right=r
            self._left=l
            return self

class pow_expr(expr):
    _content = '^'
    def differention(self):
        l = self._left.containx()
        r = self._right.containx()
        if l:
            if r:
                return pow_expr(exp_value(),mul_expr(self._right,ln_expr(self._left))).differention()
            else:
                return mul_expr(self._left.differention(),mul_expr(self._right,pow_expr(self._left,value_expr(self._right.evaluate()-1))))
        else:
            if r:
                return mul_expr(mul_expr(ln_expr(self._left),self),self._right.differention())
            else:
                return value_expr(0)

    def evaluate(self):
        return math.pow(self._left.evaluate(),self._right.evaluate())

    def _simplify(self,l,r):
        if (isinstance(r,value_expr) and r._content==0) or ( isinstance(l,value_expr) and  l._content==1):
            return value_expr(1)
        elif isinstance(l,value_expr) and l._content==0:
            return value_expr(0)
        elif isinstance(r,value_expr) and  r._content==1:
            return l
        else: 
            self._left=l
            self._right=r
            return self
    def get_node(self):
        return '('+self._left.get_node()+'^'+'('+self._right.get_node()+'))'

class ln_expr(expr):
    def __init__(self,e):
        self._content=e
        
    
    def evaluate(self):
        return value_expr(math.log(self._content.evaluate()))

    def differention(self):
        return div_expr(self._content.differention(),self._content)

    def simplify(self):
        a=self._content.simplify()
        if isinstance(a,value_expr):
            return value_expr(math.log(a._content))
        else:
            self._content=a
            return self
    
    def get_node(self):
        return "ln("+self._content.get_node()+")"




def exp_value():
    return value_expr(math.e)
        

class value_expr(expr):
    def __init__(self,val):
        self._content = val

    def differention(self):
        return value_expr(0)

    def evaluate(self):
        return self._content

    def get_node(self):
        return str(self._content)

    def simplify(self):
        return self

    def containx(self):
        return False

    def __eq__(self,a):
        return self._content==a._content

class x_expr(expr):
    _content = 'x'
    _value = 0
    def __init__(self):
        pass
    def differention(self):
        return value_expr(1)

    def evaluate(self):
        return self._value

    def get_node(self):
        return self._content

    def simplify(self):
        return self

    def set_value(self,v):
        self._value=v

    def containx(self):
        return True

    def __eq__(self,a):
        return self._content == a._content
