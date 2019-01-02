import sys
import math
import operator as op
from collections import ChainMap as Environment

special_strings = ["define", "if", "lambda"]
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


env = standard_env()


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
        except ValueError: return str(token)


def fun(attr, temp, s):

    while temp != ')':

        attr = attr + temp + ' '
        temp, s = get_identifier(s)
        if temp == '(':
            attr, s = fun(attr, temp, s)
            temp, s = get_identifier(s)

    attr += ')'
    return attr, s


def get_if_attr(s):

    attr, s = get_identifier(s)
    if attr == '(':
        attr, s = fun(attr, '', s)
        attr = attr.replace('(', ' ( ').replace(')', ' ) ')
        print("attr: ", attr)
        token, strn = get_identifier(attr)
        print("token, strn: ", token, strn)
        attr_eval, _ = eval_exp(token, strn)

    else:
        attr_eval, _ = eval_exp(attr, s)

    return attr_eval, s


def if_parser(s):

    print("If_Parser")
    test, s = get_if_attr(s)

    print("test: ", test)

    if test:
        conseq, s = get_if_attr(s)
        attr, s = get_identifier(s)
        if attr == '(':
            attr, s = fun(attr, '', s)
        print("conseq: ", conseq, "s: ", s)
        return conseq, s

    attr, s = get_identifier(s)
    if attr == '(':
        attr, s = fun(attr, '', s)
    alt, s = get_if_attr(s)
    print("alt: ", alt, "s: ", s)
    return alt, s


def define_parser(s):
    var, s = get_identifier(s)
    exp, s = get_identifier(s)
    exp_eval, s = eval_exp(exp, s)
    env[var] = exp_eval
    return None, s


def eval_exp(iden, s):

    print("idenee: ", iden, "s: ", s)

    while iden != ')':

        if iden == '(':
            iden, s = get_identifier(s)
            return eval_exp(iden, s)

        elif iden == 'define':
            proc, s = define_parser(s)
            iden, s = get_identifier(s)
            print("iden: ", iden, "s: ", s)

        elif iden == 'if':
            proc, s = if_parser(s)
            iden, s = get_identifier(s)
            print("proc_if :", proc, "s: ",s)

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
                        print("tokena: ", iden)
                        try:
                            x = env[iden]
                            print("x: ", x)
                            args.append(x)

                        except KeyError:
                            x, s = eval_exp(iden, s)
                            args.append(x)

                        print("args: ", args)
                        iden, s = get_identifier(s)

                    if iden != ')':
                        print("Invalid InputMissing )")
                        return None, s

                    print("proc: ", proc, "args: ", args)
                    try:
                        y = proc(*args)
                    except TypeError:
                        print("Type Error")
                        return None, s

                    print("y: ", y, "s: ", s)
                    return y, s

                except KeyError:
                    print("Error: Unbound symbol \'{}\'".format(x))
                    return None, s

    return proc, s


def parse_eval(s):

    iden, s = get_identifier(s)

    if iden == '(':
        iden, s = get_identifier(s)
        x, y = eval_exp(iden, s)
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
                return env[x], s
            except KeyError:
                print("Error: Unbound symbol \'{}\'".format(x))
                return None, s


if __name__ == '__main__':

    def repl():

        while True:

            s = input('>> ').replace('(', ' ( ').replace(')', ' ) ')

            if s == '':
                exit()

            result, s = parse_eval(s)
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
