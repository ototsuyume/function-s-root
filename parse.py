#! /usr/bin/python

from expr import *
from random import randint

TK_NONE = 0
TK_NUM  = 1
TK_NAME = 2
TK_OPR  = 3

x = x_expr()


opr={'+':1,'-':1,'*':2,'/':2,'^':3,'(':0,')':0}
oprexpr={'+':add_expr,'-':sub_expr,'*':mul_expr,'/':div_expr,'^':pow_expr}

nameexpr={'ln':ln_expr,'e':exp_value}

def tokenize(l):
    i=0
    j=0
    last = TK_NONE
    toklist=[]
    typelist=[]
    while j<len(l):
        if l[j]>='0' and l[j]<='9':
            if last==TK_NONE:
                last = TK_NUM
            elif last!=TK_NUM:
                typelist.append(last)
                toklist.append(l[i:j])
                last = TK_NUM 
                i=j
        elif l[j]>='a' and l[j]<='z':
            if last==TK_NONE:
                last = TK_NAME
            elif last!=TK_NAME:
                typelist.append(last)
                toklist.append(l[i:j])
                i=j
                last=TK_NAME
        elif l[j] in opr:
               typelist.append(last)
               toklist.append(l[i:j])
               last = TK_OPR
               i=j
        j=j+1
    typelist.append(last)
    toklist.append(l[i:j])         
    return (toklist,typelist)

def _parser(tokl,typel):
    i=0
    ret=0
    lastopr='+'
    nsp=0
    osp=0
    numstack=list(range(100))
    oprstack=list(range(100))
    print(tokl)
    while i<len(tokl):
        if typel[i]==TK_NUM:
            numstack[nsp]=value_expr(int(tokl[i]))
            ret = numstack[nsp]
            nsp+=1
        elif typel[i]==TK_NAME:
            if tokl[i]=='x':
                numstack[nsp] = x
                ret = x
            elif tokl[i]=='e':
                numstack[nsp] = exp_value()
                ret = numstack[nsp]
            elif tokl[i+1]!='(':
                raise Exception("Syntax error:the element after name must be a (")
            else:
                e,l=_parser(tokl[i+2:],typel[i+2:])
                numstack[nsp]=nameexpr[tokl[i]](e)
                i=i+2+l
            ret = numstack[nsp]
            nsp+=1
        
        elif typel[i]==TK_OPR:
            if tokl[i]=='(':
                i+=1
                numstack[nsp],b=_parser(tokl[i:],typel[i:])
                numstack[nsp].set_priority()
                i+=b
                nsp+=1
            elif tokl[i]==')':
                break
            
            elif osp==0:
                if nsp==0:
                    if tokl[i]!='-':
                        raise Exception("Syntax error:the head of polynomial must be a number or name")
                    numstack[nsp]=value_expr(-1)
                    oprstack[osp]='*'
                    nsp+=1
                else:
                    oprstack[osp]=tokl[i]
                osp+=1
            elif opr[tokl[i]]>opr[oprstack[osp-1]]:
                oprstack[osp]=tokl[i]
                osp+=1
            else:
                lastopr=oprstack[osp-1]
                while opr[lastopr]>=opr[tokl[i]]:
                    ret = oprexpr[lastopr](numstack[nsp-2],numstack[nsp-1]) 
                    numstack[nsp-2]=ret
                    nsp-=1
                    osp-=1
                    if osp==0:
                        break
                    lastopr=oprstack[osp-1]
                oprstack[osp]=tokl[i]
                osp+=1
        i+=1
    while osp>0:
        ret = oprexpr[oprstack[osp-1]](numstack[nsp-2],numstack[nsp-1])
        numstack[nsp-2]=ret
        nsp-=1
        osp-=1
    return (ret,i)


def find_root(l):
    tokl,typel = tokenize(l)
    a,b=_parser(tokl,typel)
    print(a)
    print("before differention:",a.get_node())
    c=a.differention()
    print("Differention:",c.get_node())

    c=c.simplify()

    print("Simplify:",c.get_node())
    d = sub_expr(x,div_expr(a,c))
    f1 = 1
    f2 = 0
    i  = 1
    while True:
        x.set_value(f1)
        f2 = d.evaluate()
        print("Iterating times:%d value:%f"%(i,f2))
        x.set_value(f2)
        if abs(a.evaluate())<=0.01:
            break
        if i>10000:
            print("Can not find a root of the function")
            break
        f1 = f2
        i+=1
    if i<=10000:
        print("The root of the function is:%f"%f2)


 
                
if __name__=='__main__':  
    find_root(sys.argv[1])
                
