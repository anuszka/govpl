# https://stackoverflow.com/questions/25936746/create-a-function-decorator-that-logs-arguments
def logger(prefix, show_first_argument=False):
    def decorate(f):
        def wrapper(*args, **kwargs):
            if show_first_argument:
                print(prefix, args[0])
            else:
                print(prefix)
            cr = f(*args, **kwargs)
            return cr
        return wrapper
    return decorate