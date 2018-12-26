import math
import operator as op

check_whitespace = [' ', '\n', '\t']


"""def remove_whitespace(s):

    i = 0
    while i < len(s) and s[i] in check_whitespace:
        i += 1
    s = s[i:]
    return s"""


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


def parser(m, s):

    if len(m) == 0 and len(s) == 0:
        print("Unexpected EOF")
        return None

    s = s[1:]
    if m == '(':

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

    elif m == ')':
        print("Unexpected )")
        return None

    else:
        x = atom(m)
        return x, s


if __name__ == '__main__':

    s = input().replace('(', ' ( ').replace(')', ' ) ')
    m, s = get_token(s)
    ps = parser(m, s)

    if ps is not None:
        s = ps[1].strip()
        if len(s) == 0:
            print(ps[0])
        else:
            print("Unexpected: ", s)

    # else:
    #    print("Incorrect Input")
