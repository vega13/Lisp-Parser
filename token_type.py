from enum import Enum


def auto_number():
    n = 0

    def auto_add_number():
        nonlocal n
        n += 1
        return n

    return auto_add_number

auto_number = auto_number()


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
    set = auto_number()                     # set
    var = auto_number()                     # var
