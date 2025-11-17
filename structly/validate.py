from functools import wraps
from typing import Any

from structly.logcall import logged


class Validator:
    def __init__(self, name=None) -> None:
        self.name = name

    def __set_name__(self, cls, name):
        self.name = name

    @classmethod
    def check(cls, value):
        return value

    def __set__(self, instance, value):
        instance.__dict__[self.name] = self.check(value)


class Typed(Validator):
    expected_type = object

    @classmethod
    def check(cls, value):
        if not isinstance(value, cls.expected_type):
            raise TypeError(f"Expected {cls.expected_type}")
        return super().check(value)


class Integer(Typed):
    expected_type = int


class Float(Typed):
    expected_type = float


class String(Typed):
    expected_type = str


class Positive(Validator):
    @classmethod
    def check(cls, value):
        if value < 0:
            raise ValueError("Expected >= 0")
        return super().check(value)


class NonEmpty(Validator):
    @classmethod
    def check(cls, value):
        if len(value) == 0:
            raise ValueError("Must be non-empty")
        return super().check(value)


class PositiveInteger(Integer, Positive):
    pass


class PositiveFloat(Float, Positive):
    pass


class NonEmptyString(String, NonEmpty):
    pass


class Stock:
    name = NonEmptyString()
    shares = PositiveInteger()
    price = PositiveFloat()

    def __init__(self, name, shares, price) -> None:
        self.name = name
        self.shares = shares
        self.price = price

    def cost(self):
        return 5

    def __set_attr__(self, name, value):
        if name not in {"name", "shares", "price"}:
            raise AttributeError("No attribute %s" % name)
        super().__setattr__(name, value)


class Proxy:
    def __init__(self, obj) -> None:
        self._obj = obj

    def __getattr__(self, name: str) -> Any:
        print(f"get {name}")
        return getattr(self._obj, name)


class ReadOnly:
    def __init__(self, obj):
        self._obj = obj

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError("can't set attribute")

    def __getattr__(self, name):
        getattr(self._obj, name)


def foo():
    """
    I print foo
    """
    print("foo")
    return 1, 2, 3


class ValidatedFunction:
    def __init__(self, func) -> None:
        self.func = func

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        for idx, arg in enumerate(args):
            varname = self.func.__code__.co_varnames[idx]
            if varname in self.func.__annotations__ and hasattr(
                self.func.__annotations__[varname], "check"
            ):
                self.func.__annotations__[varname].check(arg)
        for arg, val in kwds.items():
            if arg in self.func.__annotations__ and hasattr(
                self.func.__annotations__[arg], "check"
            ):
                self.func.__annotations__[arg].check(val)
        result = self.func(*args, **kwds)
        return result


def validated(func):
    @wraps(func)
    def wrapper(*args, **kwrgs):
        for idx, arg in enumerate(args):
            varname = func.__code__.co_varnames[idx]
            if varname in func.__annotations__ and hasattr(
                func.__annotations__[varname], "check"
            ):
                try:
                    func.__annotations__[varname].check(arg)
                except (TypeError, ValueError) as e:
                    raise TypeError(f"{varname}: {e}") from e
        for arg, val in kwrgs.items():
            if arg in func.__annotations__ and hasattr(
                func.__annotations__[arg], "check"
            ):
                try:
                    func.__annotations__[arg].check(val)
                except (TypeError, ValueError) as e:
                    raise TypeError(f"{arg}: {e}") from e

        result = func(*args, **kwrgs)
        if "return" in func.__annotations__:
            func.__annotations__["return"].check(result)
        return result

    return wrapper


def enforce(**annotations):
    def validated(func):
        @wraps(func)
        def wrapper(*args, **kwrgs):
            for idx, arg in enumerate(args):
                varname = func.__code__.co_varnames[idx]
                if varname in annotations and hasattr(annotations[varname], "check"):
                    try:
                        annotations[varname].check(arg)
                    except (TypeError, ValueError) as e:
                        raise TypeError(f"{varname}: {e}") from e
            for arg, val in kwrgs.items():
                if arg in annotations and hasattr(annotations[arg], "check"):
                    try:
                        annotations[arg].check(val)
                    except (TypeError, ValueError) as e:
                        raise TypeError(f"{arg}: {e}") from e

            result = func(*args, **kwrgs)
            if "return_" in annotations:
                annotations["return_"].check(result)
            return result

        return wrapper

    return validated


# @logged
# @logformat("{func.__code__.co_filename}:{func.__name__}")
# def add(x: PositiveInteger, y):
#     """Adds two integers"""
#     return x + y


class Spam:
    @logged
    def instance_method(self):
        pass

    @logged
    @classmethod
    def class_method(cls):
        pass

    @logged
    @staticmethod
    def static_method():
        pass

    @logged
    @property
    def property_method(self):
        pass


@enforce(return_=Integer, x=Integer, y=PositiveInteger)
def add(x, y):
    return x + y


if __name__ == "__main__":
    add(2, -3)
