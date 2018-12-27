import math
import operator as op
from collections import ChainMap as Environment


"""class Procedure(object):
    # "A user-defined Scheme procedure."

    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env

    def __call__(self, *args):
        env =  Environment(dict(zip(self.parms, args)), self.env)
        return eval(self.body, env)"""


def standard_env():

    env = {}
    env.update(vars(math))  # sin, cos, sqrt, pi, ...
    env.update({
        '+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv,
        '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq,
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


def eval(x, env):

    print("x: ", x)

    if isinstance(x, str):  # variable reference
        return env[x]

    elif not isinstance(x, list):  # constant literal
        return x

    elif isinstance(x, (int, float)):      # constant number
        return x

    elif x[0] == 'if':               # conditional
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)

    elif x[0] == 'define':           # definition
        (_, symbol, exp) = x
        env[symbol] = eval(exp, env)  # adding a new key in env with var_name as key name and the corresponding value

    else:

        print("x[0]: ", x[0])
        proc = eval(x[0], env)
        print("proc: ", proc)

        args = [eval(arg, env) for arg in x[1:]]
        print("args: ", args)
        print("proc: ", proc)
        return proc(*args)


def atom(x):

    try: 
        return int(x)
    except ValueError:
        try:
            return float(x)
        except ValueError:
            return str(x)


def get_token(s):

    token = ''
    while len(s) > 0 and s[0] == ' ':
        s = s[1:]

    while len(s) > 0 and s[0] != ' ':
        token += s[0]
        s = s[1:]

    return token, s


def parser(token, s):

    if len(token) == 0 and len(s) == 0:
        print("Unexpected EOF")
        return None

    # s = s[1:]
    if token == '(':

        lst = []
        token, s = get_token(s)

        while token != ')':

            x = (parser(token, s))
            if x is None:
                return None

            s = x[1]
            lst.append(x[0])

            token, s = get_token(s)

        return lst, s

    elif token == ')':
        print("Unexpected )")
        return None

    else:
        x = atom(token)
        return x, s


if __name__ == '__main__':

    s = input().replace('(', ' ( ').replace(')', ' ) ')
    token, s = get_token(s)
    ps = parser(token, s)

    if ps is not None:
        s = ps[1].strip()
        if len(s) == 0:
            env = standard_env()
            print(ps[0])
            # print(eval(ps[0], env))

        else:
            print("Unexpected: ", s)

    # else:
    #    print("Incorrect Input")
