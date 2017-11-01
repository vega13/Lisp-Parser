from enum import Enum


# utils
def log(*args):
    print(*args)


def auto_number():
    n = 0

    def auto_add_number():
        nonlocal n
        n += 1
        return n

    return auto_add_number

auto_number = auto_number()


def ensure(condition, message):
    # 条件成立
    if not condition:
        log('测试失败:', message)


class Stack(object):
    def __init__(self):
        super(Stack, self).__init__()
        self.list = []
        self.length = 0

    def push(self, data):
        self.list.append(data)
        self.length += 1

    def pop(self):
        data = self.list.pop(-1)
        self.length -= 1
        return data

    def __repr__(self):
        s = str(self.list)
        return s


class Type(Enum):
    auto = auto_number()                    # auto 就是 15 个特殊符号
    colon = auto_number()                   # :
    comma = auto_number()                   # ,
    brace_left = auto_number()              # {
    brace_right = auto_number()             # }
    bracket_left = auto_number()            # [
    bracket_right = auto_number()           # ]
    add = auto_number()                     # +
    min = auto_number()                     # -
    mul = auto_number()                     # *
    div = auto_number()                     # /
    mod = auto_number()                     # %
    equal = auto_number()                   # =
    not_equal = auto_number()               # !
    greater = auto_number()                 # >
    less = auto_number()                    # <
    number = auto_number()                  # 123
    string = auto_number()                  # "nice"
    yes = auto_number()                     # True
    no = auto_number()                      # False
    null = auto_number()                    # None
    log = auto_number()                     # log
    if_ = auto_number()                     # if


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


def string_end(code, index):
    escape_symbol = ['\\', '"']
    s = ''
    i = index

    while i < len(code):
        c = code[i]
        i += 1
        if c == '"':
            break
        elif c == '\\':
            c = code[i]
            if c in escape_symbol:
                s += c
                i += 1
            elif c == 't':
                s += '\t'
                i += 1
            elif code[i] == 'n':
                s += '\n'
                i += 1
            else:
                # 未定义转义，应报错
                pass
        else:
            s += c

    return s, i


def number_end(code, index):
    digits = '0123456789'
    n = code[index-1]

    while code[index] in digits:
        n += code[index]
        index += 1

    return n, index


def annotation_end(code, index):
    offset = index
    newline = '\r\n'

    while code[offset] not in newline:
        offset += 1

    end = offset + 1
    return end


def tokens(code):
    op_tokens = ['[', ']', '+', '-', '*', '/', '%', '=', '!', '>', '<']
    spaces = [' ', '\n', '\r', '\t']
    annotation = ';'
    digits = '0123456789'

    ts = []
    i = 0

    while i < len(code):
        c = code[i]
        i += 1

        if c in spaces:
            continue
        elif c in annotation:
            end = annotation_end(code, i)
            i = end
        elif c in op_tokens:
            t = Token(Type.auto, c)
            ts.append(t)
        elif c == '\"':
            s, end = string_end(code, i)
            i = end
            t = Token(Type.string, s)
            ts.append(t)
        elif c in digits:
            n, end = number_end(code, i)
            i = end
            t = Token(Type.number, n)
            ts.append(t)
        elif c == 'y':
            i += 2
            t = Token(Type.yes, 'yes')
            ts.append(t)
        elif c == 'n':
            i += 1
            t = Token(Type.no, 'no')
            ts.append(t)
        elif c == 'l':
            i += 2
            t = Token(Type.log, 'log')
            ts.append(t)
        elif c == 'i':
            i += 1
            t = Token(Type.if_, 'if')
            ts.append(t)
        else:
            # 此处应报错
            pass

    # log('json_tokens', tokens)
    return ts


def filter_tokens(stack, ts, return_token):
    op_tokens = [Type.colon, Type.comma]
    t = stack.pop()

    while True:
        if type(t) == Token:
            # 当遇到 [ 或 { 时结束
            if t.type == return_token:
                break
            # : 或 , 直接过滤
            elif t.type in op_tokens:
                t = stack.pop()
                continue

        ts.insert(0, t)
        t = stack.pop()


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
    if t.type == Type.log:
        value = 'null'
        s = ''
        for i in range(1, len(l)):
            t = l[i]
            t = Token.eval(t)
            s += t
            s += ' '
        log('>>>', s)

    return value


def apply_list(stack):
    l = []

    # 过滤特殊符号
    filter_tokens(stack, l, Type.bracket_left)
    # 对 list 求值
    value = eval_list(l)

    return value


def list_end(code, index):
    left = 1
    right = 0
    ts = []
    i = index

    while left != right:
        t = code[i]
        i += 1
        if t.type == Type.bracket_left:
            left += 1
        elif t.type == Type.bracket_right:
            right += 1
        ts.append(t)

    ts = ts[:-1]
    return ts, i


def eval_tokens(is_yes, tokens):
    t = tokens[0]
    if t.type == Type.bracket_left:
        ts, end = list_end(tokens, 1)
        if is_yes is True:
            ts = tokens[:end]
            value = _apply(ts)
            return value[0]
        else:
            ts = tokens[end:]
            t = tokens[0]
            if t.type == Type.bracket_left:
                value = _apply(ts)
                return value[0]
            else:
                return t
    else:
        if is_yes is True:
            return t
        else:
            ts = tokens[1:]
            t = ts[0]
            if t.type == Type.bracket_left:
                value = _apply(ts)
                return value[0]
            else:
                return tokens[1]


def apply_if(tokens):
    ts = []
    i = 0
    t = tokens[i]

    if t.type == Type.bracket_left:
        while t.type != Type.bracket_right:
            ts.append(t)
            i += 1
            t = tokens[i]

        is_yes = apply_list(ts)
        value = eval_tokens(is_yes, tokens[i+1:])
        return value
    elif t.type == Type.yes:
        value = eval_tokens(True, tokens[1:])
        return value
    elif t.type == Type.no:
        value = eval_tokens(False, tokens[1:])
        return value


def _apply(code, recursion=True):
    values = []
    stack = Stack()
    i = 0

    while i < len(code):
        t = code[i]
        i += 1
        # log(t, t.type)

        if t.type == Type.bracket_right:
            ts = apply_list(stack)
            stack.push(ts)
        elif t.type == Type.if_:
            # 弹出之前的 [
            stack.pop()
            ts, end = list_end(code, i)
            i = end
            value = apply_if(ts)
            stack.push(value)
        else:
            stack.push(t)

    while stack.length > 0:
        value = stack.pop()
        value = Token.eval(value)
        values.insert(0, value)

    if recursion is False:
        log('>>> ---Run finished---')
        for i in values:
            log('>>>', i)
    return values


def apply(code):
    return _apply(code, False)


def test_tokens():
    c1 = """
    [+ 1 2]
    """
    t1 = '[([), (+), (1), (2), (])]'
    ensure(str(tokens(c1)) == t1, 'test tokens 1')

    c2 = """
    [log "hello" [+ 1 2]]
    """
    t2 = '[([), (log), ("hello"), ([), (+), (1), (2), (]), (])]'
    ensure(str(tokens(c2)) == t2, 'test tokens 2')

    c3 = """
    [if yes
        [log "成功"]
        [log "没成功"]
    ]
    """
    t3 = '[([), (if), (yes), ([), (log), ("成功"), (]), ([), (log), ("没成功"), (]), (])]'
    ensure(str(tokens(c3)) == t3, 'test tokens 3')


def test_apply():
    c1 = """
    [+ 1 2]         ; 表达式的值是 3
    [* 2 3 4]       ; 表达式的值是 24
    [log "hello"]   ; 输出 hello, 表达式的值是 null(关键字 表示空)
    [+ 1 [- 2 3]]   ; 表达式的值是 0, 相当于普通语法的 1 + (2 - 3)
    [if [> 2 1] 3 4]; 表达式的值是 3
    [if yes
        [log "成功"]
        [log "没成功"]
    ]
    """
    t1 = tokens(c1)
    v1 = [3, 24, 'null', 0, 3, 'null']
    ensure(apply(t1) == v1, 'test tokens 1')


def test():
    test_tokens()
    test_apply()


def main():
    test()


if __name__ == '__main__':
    main()