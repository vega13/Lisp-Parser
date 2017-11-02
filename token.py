from token_type import Type
from utils import log


def eval_op(l):
    value = None
    op = l[0]
    op = Token.eval(op)
    l = l[1:]
    # log('op', op)
    if op in '+-*/%':
        value = l[0]
        value = Token.eval(value)
        for i in range(1, len(l)):
            t = l[i]
            t = Token.eval(t)
            if op == '+':
                value += t
            elif op == '-':
                value -= t
            elif op == '*':
                value *= t
            elif op == '/':
                value /= t
            elif op == '%':
                value %= t
    elif op in '=!><':
        a = Token.eval(l[0])
        b = Token.eval(l[1])
        # log('a b', a, b)
        if op == '=':
            value = (a == b)
        elif op == '!':
            value = (a != b)
        elif op == '>':
            value = (a > b)
        elif op == '<':
            value = (a < b)

    return value


def eval_list(l):
    value = None
    op_type = [Type.add, Type.min, Type.mul, Type.div, Type.mod, Type.equal,
               Type.not_equal, Type.greater, Type.less]
    t = l[0]
    if t.type in op_type:
        value = eval_op(l)
    elif t.type == Type.log:
        value = 'null'
        s = ''
        for i in range(1, len(l)):
            t = l[i]
            t = Token.eval(t)
            s += t
            s += ' '
        log('>>>', s)
    elif t.type == Type.if_:
        t = l[1]
        t = Token.eval(t)
        if t is True:
            value = l[2]
        else:
            value = l[3]
        value = Token.eval(value)

    return value


class Token(object):
    def __init__(self, token_type, token_value):
        super(Token, self).__init__()
        d = {
            '[': Type.bracket_left,
            ']': Type.bracket_right,
            '+': Type.add,
            '-': Type.min,
            '*': Type.mul,
            '/': Type.div,
            '%': Type.mod,
            '=': Type.equal,
            '!': Type.not_equal,
            '>': Type.greater,
            '<': Type.less,
        }
        if token_type == Type.auto:
            self.type = d[token_value]
        else:
            self.type = token_type
        self.value = token_value

    def __repr__(self):
        if self.type == Type.string:
            s = '("{}")'.format(self.value)
        else:
            s = '({})'.format(self.value)
        return s

    @staticmethod
    def type(token):
        op_type = [Type.add, Type.min, Type.mul, Type.div, Type.mod, Type.equal,
                   Type.not_equal, Type.greater, Type.less]
        token_type = type(token)
        if token_type == Token:
            if token.type in op_type:
                return token_type
            if token.type == Type.number:
                return int(token.value)
            elif token.type == Type.yes:
                return True
            elif token.type == Type.no:
                return False
            elif token.type == Type.null:
                return None
            else:
                return token_type
        else:
            return token_type

    @staticmethod
    def eval(token):
        if type(token) == Token:
            if token.type == Type.number:
                return int(token.value)
            elif token.type == Type.yes:
                return True
            elif token.type == Type.no:
                return False
            elif token.type == Type.null:
                return None
            else:
                return token.value
        elif type(token) == list:
            return eval_list(token)
        else:
            return token
