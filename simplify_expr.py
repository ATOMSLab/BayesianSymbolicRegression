from sympy import *

assuming_positive_pressure = True

def simplify_expr(expr, variables=[], parameters=[]):
    # expr is sympy operation
    # parameters: list of parameters in sympy format
    if assuming_positive_pressure and variables: # for SymPy to simplify sqrt(p)**2 
        expr = expr.subs(variables[0],symbols(str(variables[0]),positive = True))
    prime_num = [5., 7., 11., 13., 17., 19., 23., 29., 31., 37., 41., 43., 47., 53., 59., 61., 67., 71., 73., 79., 83.]
    prime_list = prime_num[0:len(parameters)]
    # substitute and simplify
    sub_expr = expr.subs([(parameters[i], prime_list[i]) for i in range(len(prime_list))]).evalf()
    try:
        # this is only for rational function, simplify the coefficient of the highest degree term
        if sub_expr.is_rational_function() \
            and ('DIV' in [i.name for i in count_ops(sub_expr,visual=True).free_symbols]): # SymPy classifies polynomial as rational
            # splitting numerator and denominator
            num, den = sub_expr.as_numer_denom()
            # finding leading coefficient of num and den
            if not num.is_constant():
                num_degree = degree(num, gen=variables[0])
                for i in LT(num).atoms(Number):
                    lead_num = i
            else:
                num_degree = 0
                lead_num = num
            den_degree = degree(den, gen=variables[0])
            den = Poly(den)
            lead_den = den.all_coeffs()[0]
            # compare the degree to decide the factor for simplification
            if num_degree > den_degree:
                factor = lead_num
            else:
                factor = lead_den
            sub_expr = (expand(num/factor))/(expand(den/factor))
            sub_expr = sub_expr.subs(1.0, 1) # SymPy doesn't reduce 1 if it is float --> convert to integer
    except:
        print('Error in simplifying this rational function to reduce 1 parameter')
    # obtain the numerical parameter after simplifying the expression
    # num_val = [a for a in sub_expr.atoms() if not a.is_Symbol]
    num_val = [a for a in sub_expr.atoms(Number)]
    # remove -1 if there is a division in the expression
    # remove 2 or -2 if pow2 presents, remove 3 or -3 if pow3 presents
    for element in [1, -1, 2, -2, 3, -3, Rational(1, 2), Rational(-1, 2)]:
        if element in num_val:
            num_val.remove(element)
    # substitute back the parameter
    constant_list = ['_c' + str(i) + '_' for i in range(len(num_val))]
    cansp = sub_expr.subs([(num_val[i], constant_list[i]) for i in range(len(num_val))])
    # rearrange constants in order of subcription number (adapted from BMS original code)
    can = str(cansp)
    ps = list([str(s) for s in cansp.free_symbols])
    positions = []
    for p in ps:
        if p.startswith('_') and p.endswith('_'):
            positions.append((can.find(p), p))
    positions.sort()
    pcount = 1
    for pos, p in positions:
        can = can.replace(p, 'c%d' % pcount)
        pcount += 1
    return can


if __name__ == '__main__':
    a0, a1, a2, a3 = symbols('a0, a1, a2, a3')
    p = symbols('p')
    # expr = (p * (a0 / ((a1 / a1) + (p / a2))))
    # expr = (p * ((p + a0) / (a3 + (p / a2))))
    # expr = sqrt(a3)
    # expr = (((a2 + a0) + p) / (((a3 / (p / a3)) + (p / a2)) + a1))
    # expr = ((a0 + p) / (((a3 / (p / a3)) + (p / a2)) + a1))
    expr = p*(p + a0) + a1 + a2/p
    print(expr)
    atomd = dict([(a.name, a) for a in expr.atoms() if a.is_Symbol])
    v_name = ['p']
    p_name = ['a0', 'a1', 'a2', 'a3']
    variables = [atomd[v] for v in v_name if v in list(atomd.keys())]
    parameters = [atomd[p] for p in p_name if p in list(atomd.keys())]
    sim_expr = simplify_expr(expr, variables, parameters)
    print(str(sim_expr).replace(' ', ''))
