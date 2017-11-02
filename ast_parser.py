from token_type import Type


def parsed_ast_process(token_list):
    """
    递归解析 ast
    """
    ts = token_list
    token = ts[0]
    del ts[0]
    if token.type == Type.bracket_left:
        exp = []
        while ts[0].type != Type.bracket_right:
            t = parsed_ast_process(ts)
            exp.append(t)
        # 循环结束, 删除末尾的 ']'
        del ts[0]
        return exp
    else:
        # token 需要 process_token / parsed_token
        return token


def parsed_ast(token_list):
    ast = []
    while len(token_list) > 0:
        ts = parsed_ast_process(token_list)
        ast.append(ts)
    return ast
