import functools


def auth(before_func, after_func=None):
    def outer(main_func):
        @functools.wraps(main_func)
        def warpper(*args, **kwargs):
            before_func()
            # if not before_result:
            #     print("返回before")
            #     return before_result
            print("开始执行被装饰的函数")
            main_result = main_func(*args, **kwargs)
            if not main_result:
                return main_result
        return warpper
    return outer
