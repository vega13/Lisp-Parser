def log(*args):
    print(*args)


def ensure(condition, message):
    # 条件成立
    if not condition:
        log('测试失败:', message)
