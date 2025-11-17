from functools import wraps


# def logged(func):
#     def wrapper(*args, **kwrgs):
#         print("Calling", func.__name__)
#         return func(*args, **kwrgs)

#     return wrapper


def logformat(format: str):
    def logged(func):
        @wraps(func)
        def wrapper(*args, **kwrgs):
            print(format.format(func=func))
            return func(*args, **kwrgs)

        return wrapper

    return logged


logged = logformat("Calling {func.__name__}")
