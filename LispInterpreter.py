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


def get_if_attr(s, env):

    attr, s = get_token(s)
    print("attr: ", attr)
    if attr == '(':
        temp, s = get_token(s)
        print("temp: ", temp)
        while temp != ')':
            attr = attr + temp + ' '
            temp, s = get_token(s)
        attr += ')'
        attr_eval, t = parser(attr[0], attr[1:], env)

    else:
        attr_eval, t = parser(attr, s, env)

    return attr_eval, s


def if_parser(s, env):

    print("Inside if Parser")
    test, s = get_if_attr(s, env)
    print("test: ", test, "s: ", s)
    conseq, s = get_if_attr(s, env)
    print("conseq: ", conseq)
    alt, s = get_if_attr(s, env)
    print("alt: ", alt)
    """test_eval, s = parser(test, s, env)
    print("test_eval: ", test_eval)"""
    if test:
        print("Conseq")
        return conseq, s
    else:
        print("Alt:")
        return alt, s


def define_parser(s, env):
    var, s = get_token(s)
    print("var: ", var)
    exp, s = get_token(s)
    print("exp: ", exp)
    eval, s = parser(exp, s, env)
    print("eval: ", eval)
    env[var] = eval
    check, s = get_token(s)
    return None, s


def eval_exp(s, env):

    token, s = get_token(s)
    if token == ')':
        return '()'

    proc, s = parser(token, s, env)
    print("proc: ", proc, "s: ", s)

    if token in special_strings:
        return proc, s

    print("proc: ", proc, "s: ", s)

    token, s = get_token(s)
    print("tokenm: ", token)

    if token == ')':
        return None, s  # (if (= 10 10) (30) (40))  (begin (define r 10) (* pi (* r r)))

    args = []
    while len(token) > 0 and token != ')':
        print("tokena: ", token)
        x, s = parser(token, s, env)
        print("x: ", x, "s: ", s)
        args.append(x)
        print("args: ", args)
        token, s = get_token(s)

    if token != ')':
        print("Missing )")
        return None, s

    try:
        return proc(*args), s
    except TypeError:
        return None, s


def parser(token, s, env):

    x = num_parser(token)
    print("x: ", x)
    if isinstance(x, (int, float)):
        print("x-:", x, "s: ", s)
        return x, s

    if x == 'define':
        print("Inside define call")
        return define_parser(s, env)

    elif x == 'if':
            print("Inside If call")
            return if_parser(s, env)

    elif x == '(':
        y, s = eval_exp(s, env)
        print("y: ", y, "s: ", s)
        return y, s

    elif x == ')':
        print("Unexpected )")
        return None

    else:
        print("x-: ", x)
        try:
            return env[x], s
        except KeyError:
            raise SyntaxError("Key Error")


if __name__ == '__main__':

    s = input().replace('(', ' ( ').replace(')', ' ) ')
    global_env = standard_env()
    token, s = get_token(s)
    result, s = parser(token, s, global_env)
    while len(s) > 0 and s[0] == ' ':
        s = s[1:]
    if len(s) == 0:
        if result is not None:
            print(result)
        else:
            print("No output")
    else:
        print("Invalid input: ", s)
