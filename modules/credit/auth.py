import functools

def auth(before_func,after_func=None):
    def outer(main_func):
        @functools.wraps(main_func)
        def warpper(*args, **kwargs):
                before_result = before_func()
                if not before_result:
                    return before_func
                main_result = main_func(*args, **kwargs)
                if not main_result:
                    return main_result
        return warpper
    return outer
