from token_type import Type


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
        else:
            return token
