import inspect
from structly.validate import Validator, validated


def validate_attributes(cls):
    _fields = tuple(
        key for key, value in cls.__dict__.items() if isinstance(value, Validator)
    )
    cls._types = tuple(getattr(cls, field).expected_type for field in _fields)
    cls._fields = _fields
    for attr, method in cls.__dict__.items():
        if inspect.isfunction(method):
            setattr(cls, attr, validated(method))

    cls.create_init()
    return cls


class Structure:
    _fields = ()
    _types = ()

    def __iter__(self):
        for i in self._fields:
            yield getattr(self, i)

    def __eq__(self, other):
        return isinstance(other, type(self)) and tuple(self) == tuple(other)

    @classmethod
    def from_row(cls, row):
        rowdata = [func(val) for func, val in zip(cls._types, row)]
        return cls(*rowdata)

    @classmethod
    def __init_subclass__(cls):
        validate_attributes(cls)

    @classmethod
    def create_init(cls):
        argstr = ",".join(cls._fields)
        code = f"def __init__(self, {argstr}):\n"
        for arg in cls._fields:
            code += f"    self.{arg} = {arg}\n"
        locs = {}
        exec(code, locs)
        cls.__init__ = locs["__init__"]

    def __repr__(self):
        return f"{type(self).__name__}({', '.join((repr(getattr(self, key)) for key in self._fields))})"

    def __setattr__(self, key, val):
        if isinstance(key, str):
            if key.startswith("_") or key in self._fields:
                return super().__setattr__(key, val)
            raise AttributeError(f"only attributes in {self._fields} are allowed")


def add(x, y=0):
    "Add two numbers"
    return x + y


__all__ = ["Structure"]
