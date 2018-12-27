import math
import operator as op


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

    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError: return str(token)


def define_parser(s, env):
    var, s = get_token(s)
    print("var: ", var)
    exp, s = get_token(s)
    print("exp: ", exp)
    eval, s = parser(exp, s, env)
    print("eval: ", eval)
    env[var] = eval
    return None, s


def eval_exp(s, env):

    token, s = get_token(s)
    print("tokenp: ", token)
    if token != ')':
        proc, s = parser(token, s, env)
        print("proc: ", proc, "s: ", s)

    token, s = get_token(s)
    print("tokenm: ", token)

    if token == ')':
        return None, s

    args = []
    while len(token) > 0 and token != ')':
        print("tokena: ", token)
        x, s = parser(token, s, env)
        print("x: ", x, "s: ", s)
        args.append(x)
        print("args: ", args)
        token, s = get_token(s)

    if token!= ')':
        return None, s

    try:
        return proc(*args), s
    except TypeError:
        return None, s


def parser(token, s, env):

    x = num_parser(token)
    if isinstance(x, (int, float)):
        print("x-:", x, "s: ", s)
        return x, s

    if x == 'define':
        print("Inside define call")
        return define_parser(s, env)

    # elif x == 'if':
    #    if_parser(s)

    elif x == '(':
        y, s = eval_exp(s, env)
        print("y: ", y, "s: ", s)
        return y, s

    elif x == ')':
        print("Unexpected )")
        return None

    else:
        return env[x], s


if __name__ == '__main__':
    s = input().replace('(', ' ( ').replace(')', ' ) ')
    global_env = standard_env()
    token, s = get_token(s)
    result = parser(token, s, global_env)
    print("result-: ", result[0])
