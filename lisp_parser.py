from token_parser import tokens
from token import Token
from ast_parser import parsed_ast
from utils import log, ensure


def _apply(code, var_list, recursion=True):
    ts = code
    l = []

    while len(ts) > 0:
        token = ts[0]
        del ts[0]

        if type(token) == list:
            t = Token.eval(token, var_list)
            l.append(t)
        else:
            l.append(token)

    if recursion is False:
        log('>>> ---Run finished---')
        for i in l:
            log('>>>', i)

    log()
    return l


def apply(code):
    var_list = {}
    return _apply(code, var_list, False)


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
    ensure(apply(a1) == v1, 'test tokens 1')

    c2 = """
    [set a 1]
    [set b 2]
    [set c [+ a b]]
    [+ a b c]
    """
    t2 = tokens(c2)
    a2 = parsed_ast(t2)
    v2 = [1, 2, 3, 6]
    ensure(apply(a2) == v2, 'test tokens 2')


def test():
    test_tokens()
    test_apply()


def main():
    test()


if __name__ == '__main__':
    main()
