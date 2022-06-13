# this function is to check the thermodynamic constraints of the function. There are 3 outputs: 
# 1) the Boolean   2) The name of the constraint it violates 3) The expression if SymPy fails to evaluate the constraint. 

import sympy as sp
import numpy as np
import sys

"""
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
"""


def is_monotonic_increasing(expr, interval, var):

    # constant value never decreases    
    if expr.is_constant():
        return True

    print("type of expression =", type(expr))

    # get critical points as list
    turning_points = list(sp.solveset(expr.diff(var), var, interval))
    turning_points.sort()
    # failed to find critical points
    # there could be 0 or infinite...
    if (turning_points == []):
        print("no turning points...")
        # fall back to simpler increasing function
        return bool(1 if (expr.limit(var, interval.end) - expr.limit(var, interval.start)) >= 0 else 0)
    increasing = 1
    # turn to false if interval from start of main interval to first critical point not increasing
    increasing = min(increasing, (1 if (expr.limit(var, turning_points[0]) - expr.limit(var, interval.start)) >= 0 else 0))
    # check intervals between all critical points
    for i in range(len(turning_points)-1):
        thisPoint = turning_points[i]
        nextPoint = turning_points[i+1]
        increasing = min(increasing, (1 if (expr.limit(var, nextPoint) - expr.limit(var, thisPoint)) >= 0 else 0))
        #increasing = min(increasing, sympy.is_increasing(expr, sympy.Interval(thisPoint, nextPoint, false, false), var))
    # check last interval
    increasing = min(increasing, (1 if (expr.limit(var, interval.end) - expr.limit(var, turning_points[-1])) >= 0 else 0))
    #increasing = min(increasing, sympy.is_increasing(expr, sympy.Interval(turning_points[-1], interval.end, false, false), var))
    return bool(increasing)

# no parameters to fill variant
def sym_thermo_constraint(expr, var, par):

    prime_num = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83]
    prime_list = prime_num[0:len(par)]
    # substitute and simplify
    sub_expr = expr.subs([(par[i], prime_list[i]) for i in range(len(prime_list))]).evalf()

    #print(sub_expr)
    
    results = [True, True, True]

    
    # Axiom 1: the expr needs to pass through the origin
    try:
        if sp.limit(sub_expr, var, 0, "+") != 0:
            #println("constraint 1")
            results[0] = False
    except:
        #println(error)
        print("SymPy cannot evaluate Axiom 1")
        results[0] = False
    # Axiom 2: the expr needs to converge to Henry's Law at zero pressure
    try:
        if (sp.limit(sp.diff(sub_expr, var), var, 0) == sp.oo 
            or sp.limit(sp.diff(sub_expr, var), var, 0) == -sp.oo 
            or sp.limit(sp.diff(sub_expr, var), var, 0) == 0):
            #println("constraint 2")
            results[1] = False
    except:
        #println(error)
        print("SymPy cannot evaluate Axiom 2")
        results[1] = False

    # Axiom 3: the expr must be strictly increasing as pressure increases
    try:
        # use custom function because sympy doesn't work as expected
        if not(is_monotonic_increasing(sub_expr, sp.Interval(0,sp.oo), var)):
            #println("constraint 3")
            results[2] = False
    except:
        print("SymPy cannot evaluate Axiom 3")
        print("Oops!", sys.exc_info()[0], "occurred for", sub_expr)
        results[2] = False

    #print(results)
    return results




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