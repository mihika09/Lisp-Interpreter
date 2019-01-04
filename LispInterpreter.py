import sys
import math
import operator as op
from collections import ChainMap as Environment

special_strings = ["define", "if", "lambda"]
sys.setrecursionlimit(3000)


class Procedure(object):

    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env

    def __call__(self, *args):
        env = Environment(dict(zip(self.parms, args)), self.env)
        x, t = get_identifier(self.body)
        px, sx = eval_exp(x, t, env)
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
        'append': op.add,
        'expt': op.pow,
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


def get_identifier(s):

    iden = ''
    while len(s) > 0 and s[0] == ' ':
        s = s[1:]

    while len(s) > 0 and s[0] != ' ':
        iden += str(s[0])
        s = s[1:]

    return iden, s


def num_parser(token):

    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return str(token)


def fun(attr, temp, s):

    while temp != ')':

        attr = attr + temp + ' '
        temp, s = get_identifier(s)
        if temp == '(':
            attr, s = fun(attr, temp, s)
            temp, s = get_identifier(s)

    attr += ')'
    return attr, s


def get_if_attr(s, env):

    attr, s = get_identifier(s)
    if attr == '(':
        attr, s = fun(attr, '', s)
        attr = attr.replace('(', ' ( ').replace(')', ' ) ')
        print("attr: ", attr)
        token, strn = get_identifier(attr)
        print("token, strn: ", token, strn)
        attr_eval, _ = eval_exp(token, strn, env)

    else:
        attr_eval, _ = eval_exp(attr, s, env)

    return attr_eval, s


def if_parser(s, env):

    print("If_Parser")
    test, s = get_if_attr(s, env)

    print("test: ", test)

    if test:
        conseq, s = get_if_attr(s, env)
        attr, s = get_identifier(s)
        if attr == '(':
            attr, s = fun(attr, '', s)
        print("conseq: ", conseq, "s: ", s)
        return conseq, s

    attr, s = get_identifier(s)
    if attr == '(':
        attr, s = fun(attr, '', s)
    alt, s = get_if_attr(s, env)
    print("alt: ", alt, "s: ", s)
    return alt, s


def define_parser(s, env):
    var, s = get_identifier(s)
    print("var: ", var)
    exp, s = get_identifier(s)
    print("exp: ", exp)
    exp_eval, s = eval_exp(exp, s, env)
    print("exp_eval: ", exp_eval)
    env[var] = exp_eval
    print("var: ", var)
    print("env[var]: ", env[var])
    print("s_define: ", s)
    return None, s


def funl(attr, temp, s):

    count = 1
    while count != 0:

        attr = attr + temp + ' '
        temp, s = get_identifier(s)
        if temp == '(':
            count += 1
        elif temp == ')':
            count -= 1

    attr += ')'
    print("attr_lambda: ", attr, "s: ", s)
    return attr, s


def get_lambda_attr(s):
    attr, s = get_identifier(s)
    if attr == '(':
        attr, s = funl(attr, '', s)
        attr = attr.replace('(', ' ( ').replace(')', ' ) ')
        # print("attr after: ", attr)

    return attr, s


def lambda_parser(s, env):

    print("Lambda Parser")
    parms, s = get_lambda_attr(s)
    body, s = get_lambda_attr(s)
    parms = list(parms.split())
    parms = parms[1]
    print("parms: ", parms, "body: ", body, "s: ", s)
    return Procedure(parms, body, env), s


def quote_parser(s, env):

    print("Quote Parser")
    attr, s = get_identifier(s)

    if attr == '(':
        attr = s[0:s.index(')')]
        s = s[s.index(')')+1:]
        print("attr: ", attr)

    return attr, s


def get_args(s, env):

    iden, s = get_identifier(s)
    args = []
    print("iden: ", iden, "args: ", args)

    while len(iden) > 0 and iden != ')':
        print("tokena: ", iden, "s: ", s)
        try:
            x = env[iden]
            print("x: ", x)
            args.append(x)

        except KeyError:
            x, s = eval_exp(iden, s, env)
            args.append(x)

        print("args: ", args)
        iden, s = get_identifier(s)

    if iden != ')':
        print("Invalid InputMissings )")
        return None, s

    return args, s


def eval_exp(iden, s, env):

    print("idenee: ", iden, "s: ", s)

    while iden != ')':

        if iden == '(':
            iden, s = get_identifier(s)
            proc, s = eval_exp(iden, s, env)
            print("p: ", proc, "s: ", s)
            args, s = get_args(s, env)

            if args is None:
                return None, s

            elif len(args) == 0:
                iden = ')'

            else:
                print("proc: ", proc, "args: ", args, "s: ", s)
                try:
                    y = proc(*args)
                    print("y p(*a): ", y, "s: ", s)
                except TypeError:
                    print("Type Error")
                    return None, s

                print("y: ", y, "s: ", s)
                return y, s

        elif iden == 'define':
            proc, s = define_parser(s, env)
            # iden, s = get_identifier(s)
            return proc, s
            print("iden_define: ", iden, "s: ", s)

        elif iden == 'if':
            proc, s = if_parser(s, env)
            # iden, s = get_identifier(s)

            print("proc_if :", proc, "s: ", s)
            return proc, s

        elif iden == 'lambda':
            proc, s = lambda_parser(s, env)

            print("proc_lambda: ", proc, "s: ", s)
            return proc, s

        elif iden == 'quote':
            proc, s = quote_parser(s, env)
            print("proc: ", proc, "s: ", s)
            iden, s = get_identifier(s)

        else:
            x = num_parser(iden)
            if isinstance(x, (int, float)):
                return x, s

            else:
                try:
                    print("env[x]: ", env[x])
                    proc = env[x]
                    if isinstance(proc, (int, float)):
                        # invalid as '(' needs to be followed by a procedure
                        return None, s

                    print("proc: ", proc, "s: ", s)

                    iden, s = get_identifier(s)
                    args = []
                    print("iden: ", iden, "args: ", args)
                    while len(iden) > 0 and iden != ')':
                        print("tokena: ", iden, "s: ", s)
                        try:
                            x = env[iden]
                            print("x: ", x)
                            args.append(x)

                        except KeyError:
                            x, s = eval_exp(iden, s, env)
                            args.append(x)

                        print("args: ", args)
                        iden, s = get_identifier(s)

                    if iden != ')':
                        print("Invalid InputMissing )")
                        return None, s

                    print("proc: ", proc, "args: ", args, "s: ", s)
                    try:
                        y = proc(*args)
                        print("y p(*a): ", y, "s: ", s)
                    except TypeError:
                        print("Type Error")
                        return None, s

                    print("y: ", y, "s: ", s)
                    return y, s

                except KeyError:
                    print("Error: Unbound symbols \'{}\'".format(x))
                    return None, s

    return proc, s


def parse_eval(s, env):

    iden, s = get_identifier(s)

    if iden == '(':
        # iden, s = get_identifier(s)
        x, y = eval_exp(iden, s, env)
        print("x: ", x, "y: ", y)
        return x, y
        # return None, s

    elif iden == ')':
        print("Unexpected )")
        return None, s

    else:
        x = num_parser(iden)
        if isinstance(x, (int, float)):
            return x, s

        else:
            try:
                print("x: ", x)
                print("env[x]: ", env[x])
                return env[x], s
            except KeyError:
                print("Error: Unbound symbols \'{}\'".format(x))
                return None, s


if __name__ == '__main__':

    def repl():

        global_env = standard_env()
        while True:

            s = input('>> ').replace('(', ' ( ').replace(')', ' ) ')

            if s == '':
                exit()

            result, s = parse_eval(s, global_env)
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
            try:
                return str(exp)
            except TypeError:
                return str(exp)

    repl()
