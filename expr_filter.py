# NOT USE FOR NOW #

# This function filters the complicated expression resulting from SR that SYMPY can't handle
list_filter = ['p**', 'p)**']

def expr_filter(str_expr, filter_str):
    index = str_expr.find(filter_str)
    if index == -1:
        return True
    else:
        if str_expr[index+len(filter_str)] == '(':
            paren_count = 0
            char_count = 0
            paren_open = []
            paren_pair = []
            while paren_count >= 0 and char_count < len(str_expr[index+len(filter_str):]):
                if str_expr[index+len(filter_str):][char_count] == '(':
                    paren_count += 1
                    paren_open.append(char_count)
                elif str_expr[index+len(filter_str):][char_count] == ')':
                    paren_count -= 1
                    paren_pair.append((paren_open[-1], char_count))
                    del paren_open[-1]
                char_count += 1
            if str_expr[index+len(filter_str):][paren_pair[0][0]:paren_pair[0][1]].find('p') != -1:
                return False
            else:
                return True
        elif str_expr[index+len(filter_str)] == 'p':
            return False
        else:
            return True


if __name__ == '__main__':
    for filter_str in list_filter:
        expr_s1 = '18.1379058761851*p**(p**(-15.1674989574457/p))'
        print(expr_filter(expr_s1, filter_str))
        if expr_filter(expr_s1, filter_str) is False:
            break
    for filter_str in list_filter:
        expr_s2 = '21.7727273000359*p**(1607.51458850793*1607.51458850793**(-2*p))'
        print(expr_filter(expr_s2, filter_str))
        if expr_filter(expr_s2, filter_str) is False:
            break

    for filter_str in list_filter:
        expr_s3 = '(2.99192010654965*p)**(1.38999912544184*(p + 1.0622245063956e-6)**(-0.1730403993765))'
        print(expr_filter(expr_s3, filter_str))
        if expr_filter(expr_s3, filter_str) is False:
            break
