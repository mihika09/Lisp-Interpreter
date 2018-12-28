import math
import operator as op

special_strings = ["define", "if"]


def standard_env():

    env = {}
    env.update(vars(math))  # sin, cos, sqrt, pi, ...
    env.update({
        '+': op.add,
        '-': op.sub,
        '*': op.mul,
        '/': op.truediv,
        '>': op.gt,
        '<': op.lt,
        '>=': op.ge,
        '<=': op.le,
        '=': op.eq,
        'abs': abs,
        'append': op.add,
        'apply': lambda proc, args: proc(*args),
        'begin': lambda *x: x[-1],
        'car': lambda x: x[0],
        'cdr': lambda x: x[1:],
        'cons': lambda x, y: [x] + y,
        'eq?': op.is_,
        'equal?': op.eq,
        'length': len,
        'list': lambda *x: list(x),
        'list?': lambda x: isinstance(x,list),
        'map': lambda *args: list(map(*args)),
        'max': max,
        'min': min,
        'not': op.not_,
        'null?': lambda x: x == [],
        'number?': lambda x: isinstance(x, (int, float)),
        'procedure?': callable,
        'round': round,
        'symbol?': lambda x: isinstance(x, str),
    })
    return env


def get_token(s):

    token = ''
    while len(s) > 0 and s[0] == ' ':
        s = s[1:]

    while len(s) > 0 and s[0] != ' ':
        token += s[0]
        s = s[1:]

    return token, s


def num_parser(token):

    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError: return str(token)


def fun(attr, temp, s):

    while temp != ')':

        attr = attr + temp + ' '
        temp, s = get_token(s)
        if temp == '(':
            attr, s = fun(attr, temp, s)
            temp, s = get_token(s)

    attr += ')'
    return attr, s


def get_if_attr(s, env):

    attr, s = get_token(s)
    if attr == '(':
        attr, s = fun(attr, '', s)
        attr = attr.replace('(', ' ( ').replace(')', ' ) ')
        token, strn = get_token(attr)
        attr_eval, _ = parser(token, strn, env)

    else:
        attr_eval, _ = parser(attr, s, env)

    return attr_eval, s


def if_parser(s, env):

    test, s = get_if_attr(s, env)
    conseq, s = get_if_attr(s, env)
    alt, s = get_if_attr(s, env)
    if test:
        _, s = get_token(s)
        return conseq, s
    else:
        _, s = get_token(s)
        return alt, s


def define_parser(s, env):
    var, s = get_token(s)
    exp, s = get_token(s)
    eval, s = parser(exp, s, env)
    env[var] = eval
    check, s = get_token(s)
    return None, s


def eval_exp(s, env):

    token, s = get_token(s)
    if token == ')':
        return '()'

    proc, s = parser(token, s, env)

    if token in special_strings:
        return proc, s

    token, s = get_token(s)

    if token == ')':
        return None, s

    args = []
    while len(token) > 0 and token != ')':
        x, s = parser(token, s, env)
        args.append(x)
        token, s = get_token(s)

    if token != ')':
        print("Invalid InputMissing )")
        return None, s

    try:
        return proc(*args), s
    except TypeError:
        return None, s


def parser(token, s, env):

    x = num_parser(token)
    if isinstance(x, (int, float)):
        return x, s

    if x == 'define':
        return define_parser(s, env)

    elif x == 'if':
        return if_parser(s, env)

    elif x == '(':
        y, s = eval_exp(s, env)
        return y, s

    elif x == ')':
        print("Unexpected )")
        return None

    else:
        if x == '':
            exit()
        try:
            return env[x], s
        except KeyError:
            return x, s


if __name__ == '__main__':

    def repl():

        global_env = standard_env()
        while True:
            s = input('>> ').replace('(', ' ( ').replace(')', ' ) ')
            token, s = get_token(s)
            result, s = parser(token, s, global_env)
            while len(s) > 0 and s[0] == ' ':
                s = s[1:]

            if len(s) == 0:
                if result is not None:
                    print(schemestr(result))

            else:
                print("Invalid Input")


    def schemestr(exp):

        if isinstance(exp, list):
            return '(' + ' '.join(map(schemestr, exp)) + ')'
        else:
            return str(exp)

    repl()
