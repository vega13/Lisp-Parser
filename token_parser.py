from token_type import Type
from token import Token


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


def var_end(code, index):
    i = index
    spaces = [' ', '\n', '\r', '\t', '[', ']']
    s = ''
    c = code[i]
    while c not in spaces:
        s += c
        i += 1
        c = code[i]
    return s, i


def tokens(code):
    op_tokens = ['[', ']', '+', '-', '*', '/', '%', '=', '!', '>', '<']
    spaces = [' ', '\n', '\r', '\t']
    annotation = ';'
    digits = '0123456789'
    var_start = 'abcdefghijklmnopqrstuvwxyz'

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
        elif c == 'y' and code[i:i+2] == 'es':
            i += 2
            t = Token(Type.yes, 'yes')
            ts.append(t)
        elif c == 'n' and code[i:i+1] == 'o':
            i += 1
            t = Token(Type.no, 'no')
            ts.append(t)
        elif c == 'l' and code[i:i+2] == 'og':
            i += 2
            t = Token(Type.log, 'log')
            ts.append(t)
        elif c == 'i' and code[i:i+1] == 'f':
            i += 1
            t = Token(Type.if_, 'if')
            ts.append(t)
        elif c == 's' and code[i:i+2] == 'et':
            i += 2
            t = Token(Type.set, 'set')
            ts.append(t)
        elif c in var_start:
            s, end = var_end(code, i - 1)
            i = end
            t = Token(Type.var, s)
            ts.append(t)
        else:
            # 此处应报错
            pass

    # log('json_tokens', tokens)
    return ts
