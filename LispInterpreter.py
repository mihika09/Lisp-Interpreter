import math
import operator as op

check_whitespace = [' ', '\n', '\t']


def remove_whitespace(s):

    i = 0
    while i < len(s) and s[i] in check_whitespace:
        i += 1
    s = s[i:]
    return s


def atom(x):

    print("atom(x): ", x)
    try: 
        return int(x)
    except ValueError:
        try:
            return float(x)
        except ValueError:
            return str(x)


"""def parser(m, s):

    if len(s) == 0:
        raise SyntaxError("Unexpected EOF")

    print("m: ", m, "s: ", s)

    # s = s.strip()

    if m == '(':

        lst = []
        i = 1

        token = ''
        while i < len(s) and s[i] == ' ':
            i += 1

        while i < len(s) and s[i] != ' ':
            token += s[i]
            i += 1

        print("token: ", token)
        print("i: ", i, "s[i]: ", s[i])

        while token != ')':

            lst.append(parser(token, s[i:]))
            print("lst: ", lst)
            print("i: ", i, "len(s): ", len(s), "s[i]: ", s[i])

            token = ''
            while i < len(s) and s[i] == ' ':
                i += 1

            while i < len(s) and s[i] != ' ':
                token += s[i]
                i += 1

        return lst"""


def parser(m, s):

    if len(s) == 0:
        raise SyntaxError("Unexpected EOF")

    print("m: ", m, "s: ", s)

    s = s[1:]
    if m == '(':

        lst = []

        token = ''
        while len(s) > 0 and s[0] == ' ':
            s = s[1:]

        while len(s) > 0 and s[0] != ' ':
            token += s[0]
            s = s[1:]

        print("token: ", token)
        print("s[0]: ", s[0])

        while token != ')':

            x, s = (parser(token, s))
            lst.append(x)
            print("lst: ", lst)
            print("len(s): ", len(s), "s[0]: ", s[0])

            token = ''
            while len(s) > 0 and s[0] == ' ':
                s = s[1:]

            while len(s) > 0 and s[0] != ' ':
                token += s[0]
                s = s[1:]

            print("token#: ", token)

        return lst, s

    elif m == ')':
        raise SyntaxError("Unexpected EOF")

    else:
        x = atom(m)
        print("Return value of atom(): ", x)
        return x, s


if __name__ == '__main__':

    s = input()
    s = s.replace('(', ' ( ').replace(')', ' ) ')
    print("s: ", s)
    s = remove_whitespace(s)
    ps = parser(s[0], s)
    print(ps)
