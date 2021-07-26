# this function is to check the thermodynamic constraints of the function. There are 3 outputs: 
# 1) the Boolean   2) The name of the constraint it violates 3) The expression if SymPy fails to evaluate the constraint. 

import sympy as sp
import numpy as np

def sym_thermo_constraint(expr, var, par):
    prime_num = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83]
    prime_list = prime_num[0:len(par)]
    # substitute and simplify
    sub_expr = expr.subs([(par[i], prime_list[i]) for i in range(len(prime_list))]).evalf()
    # Axiom 1: the expr needs to pass through the origin
    try:
        if sp.limit(sub_expr, var, 0, '+') != 0:
            return False, 'Axiom 1', ''
    except:
        print('SymPy cannot evaluate Axiom 1')
        return False, 'Axiom 1', expr
    # Axiom 2: the expr needs to converge to Henry's Law at zero pressure
    try:
        if sp.limit(sp.diff(sub_expr, var), var, 0) == sp.oo \
                or sp.limit(sp.diff(sub_expr, var), var, 0) == -sp.oo \
                or sp.limit(sp.diff(sub_expr, var), var, 0) == 0:
            return False, 'Axiom 2', ''
    except:
        print('SymPy cannot evaluate Axiom 2')
        return False, 'Axiom 2', expr
    return True, '', ''

if __name__ == '__main__':
    p, x, a, b = sp.symbols('p,x,a,b')
    _a0_, _a1_, _a2_, _a3_ = sp.symbols('_a0_, _a1_, _a2_, _a3_')
    expr1 = sp.sqrt(p)*a
    print(sym_thermo_constraint(expr1, p, [a]))
    expr2 = a*x/(b+x)
    print(sym_thermo_constraint(expr2, x, [a,b]))
    expr3 = a*x**x
    print(sym_thermo_constraint(expr3, x, [a]))
    expr4 = (a*x)/(b+x)+a
    print(sym_thermo_constraint(expr4, x, [a,b]))
    expr5 = ((((-(_a2_) / (x + sp.sqrt(_a0_))) * _a1_) + sp.sqrt(((x ** 2) * x))) * (_a2_ + x))
    print(sym_thermo_constraint(expr5, x, [_a0_, _a1_, _a2_, _a3_]))