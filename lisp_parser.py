from token_parser import tokens
from token_type import Type
from token import Token
from ast_parser import parsed_ast
from utils import log, ensure


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


def filter_tokens(stack, return_token):
    ts = []
    op_tokens = [Type.colon, Type.comma]
    t = stack.pop()

    while True:
        if type(t) == Token:
            # 当遇到 [ 或 { 时结束
            if t.type == return_token:
                return ts
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
    elif t.type == Type.log:
        value = 'null'
        s = ''
        for i in range(1, len(l)):
            t = l[i]
            t = Token.eval(t)
            s += t
            s += ' '
        log('>>>', s)

    return value


def apply_list(stack, var_list=None):
    # 过滤特殊符号
    l = filter_tokens(stack, Type.bracket_left)
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


def eval_tokens(is_yes, token_list):
    t = token_list[0]
    if t.type == Type.bracket_left:
        ts, end = list_end(token_list, 1)
        if is_yes is True:
            ts = token_list[:end]
            value = _apply(ts)
            return value[0]
        else:
            ts = token_list[end:]
            t = token_list[0]
            if t.type == Type.bracket_left:
                value = _apply(ts)
                return value[0]
            else:
                return t
    else:
        if is_yes is True:
            return t
        else:
            ts = token_list[1:]
            t = ts[0]
            if t.type == Type.bracket_left:
                value = _apply(ts)
                return value[0]
            else:
                return token_list[1]


def apply_if(token_list):
    ts = []
    i = 0
    t = token_list[i]

    if t.type == Type.bracket_left:
        while t.type != Type.bracket_right:
            ts.append(t)
            i += 1
            t = token_list[i]

        is_yes = apply_list(ts)
        value = eval_tokens(is_yes, token_list[i+1:])
        return value
    elif t.type == Type.yes:
        value = eval_tokens(True, token_list[1:])
        return value
    elif t.type == Type.no:
        value = eval_tokens(False, token_list[1:])
        return value


def _apply(code, var_list=None, recursion=True):
    values = []
    stack = Stack()
    i = 0

    while i < len(code):
        t = code[i]
        i += 1
        # log(t, t.type)

        if t.type == Type.bracket_right:
            ts = apply_list(stack, var_list)
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
    var_list = {}
    # return _apply(code, var_list, False)
    return _apply(code, var_list, True)


def ast_apply(code):
    ts = code
    l = []

    while len(ts) > 0:
        token = ts[0]
        del ts[0]

        if type(token) == list:
            t = Token.eval(token)
            l.append(t)
        else:
            l.append(token)

    return l


def test_tokens():
    c1 = '''
        [set a 1]
        [set b 2]
        [+ a b]
    '''
    t1 = '[([), (set), (a), (1), (]), ([), (set), (b), (2), (]), ([), (+), (a), (b), (])]'
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
    a1 = parsed_ast(t1)
    v1 = [3, 24, 'null', 0, 3, 'null']
    ensure(ast_apply(a1) == v1, 'test tokens 1')

    # c2 = """
    # [set a 1]
    # [set b 2]
    # [+ a b]
    # """
    # t2 = tokens(c2)
    # log('tokens', t2)
    # a2 = parsed_ast(t2)
    # log('parsed_ast', a2)
    # v2 = [1, 2, 3]
    # log(apply(t2))
    # ensure(apply(t2) == v2, 'test tokens 1')


def test():
    test_tokens()
    test_apply()


def main():
    test()


if __name__ == '__main__':
    main()
