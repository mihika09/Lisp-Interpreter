import sys
import math
import operator as op
from collections import ChainMap as Environment

special_strings = ["define", "if", "lambda", "quote"]
sys.setrecursionlimit(2000)


class Procedure(object):

    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env

    def __call__(self, *args):
        env = Environment(dict(zip(self.parms, args)), self.env)
        x, t = get_token(self.body)
        px, sx = parser(x, t, env)
        return px


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
        'expt':op.pow,
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
        token += str(s[0])
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

    if test:
        conseq, s = get_if_attr(s, env)
        attr, s = get_token(s)
        if attr == '(':
            attr, s = fun(attr, '', s)
        _, s = get_token(s)
        return conseq, s

    attr, s = get_token(s)
    if attr == '(':
        attr, s = fun(attr, '', s)
    alt, s = get_if_attr(s, env)
    _, s = get_token(s)
    return alt, s


def get_lambda_attr(s, env):
    attr, s = get_token(s)
    if attr == '(':
        attr, s = fun(attr, '', s)
        attr = attr.replace('(', ' ( ').replace(')', ' ) ')
        # print("attr after: ", attr)

    return attr, s


def get_parms(s, env):



def lambda_parser(s, env):

    parms, s = get_lambda_attr(s, env)
    body, s = get_lambda_attr(s, env)
    parms = list(parms.split())
    parms = gt_parms(parms)
    _, s = get_token(s)
    print("parms: ", parms, "body: ", body, "s: ", s)
    return Procedure(parms, body, env), s


def define_parser(s, env):
    var, s = get_token(s)
    print("var: ", var, "s: ", s)
    exp, s = get_token(s)
    print("exp: ", exp, "s: ", s)
    eval_exp, s = parser(exp, s, env)
    print("eval_Exp: ", eval_exp, "s: ", s)
    env[var] = eval_exp
    _, s = get_token(s)
    return None, s


def quote_parser(s):

    print("s: ", s)
    iden, s = get_token(s)
    print("iden: ", iden, "s: ", s)
    if iden == '(':
        y = iden
        while len(s) > 0 and y != ')':
            y, s = get_token(s)
            print("y: ", y, "s: ", s)
            iden = iden + y + ' '
            print("iden: ", iden)

    _, s = get_token(s)

    print("iden: ", iden, "s: ", s)
    return iden, s


def eval_exp(s, env):

    token, s = get_token(s)
    print("tokenp: ", token)
    if token == ')':
        return '()'

    proc, s = parser(token, s, env)
    print("proc: ", proc, "s: ", s)

    if token in special_strings:
        print("Hey")
        return proc, s

    token, s = get_token(s)

    if token == ')':
        return None, s

    args = []
    while len(token) > 0 and token != ')':
        print("tokena: ", token)
        x, s = parser(token, s, env)
        args.append(x)
        print("args: ", args)
        token, s = get_token(s)

    if token != ')':
        print("Invalid InputMissing )")
        return None, s

    return proc(*args), s


def parser(token, s, env):

    x = num_parser(token)
    print("x: ", x)

    if isinstance(x, (int, float)):
        return x, s

    if x == 'define':
        return define_parser(s, env)

    elif x == 'lambda':
        return lambda_parser(s, env)

    elif x == 'if':
        return if_parser(s, env)

    elif x == 'quote':
        return quote_parser(s)

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

            print("s: ", s)
            if len(s) == 0:
                if result is not None:
                    print("result: ", schemestr(result))

            else:
                print("Invalid Inputs")


    def schemestr(exp):

        if isinstance(exp, list):
            return '(' + ' '.join(map(schemestr, exp)) + ')'
        else:
            try: return str(exp)
            except TypeError:
                return str(exp)

    repl()
