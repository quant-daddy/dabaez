from typing import Protocol
from structly.logcall import logged


@logged
def add(x, y):
    return x + y


@logged
def _sub(x, y):
    return x - y


def frange(start, stop, step):
    val = start
    while val < stop:
        yield val
        val += step


class FRange:
    def __init__(self, start, stop, step) -> None:
        self.start = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        val = self.start
        while val < self.stop:
            yield val
            val += self.step


class Writable(Protocol):
    def write(self, data: str) -> None: ...


def write(writer: Writable):
    writer.write("hello")


class Descriptor:
    def __init__(self, name) -> None:
        self.name = name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        print("%s:__get__" % self.name)
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        print("%s:__set__ %s" % (self.name, str(value)))
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        print("%s:__delete__" % self.name)


class Foo:
    a = Descriptor("a")

    def __init__(self, a) -> None:
        self.a = a


if __name__ == "__main__":

    class Writer:
        def write(self, data: str):
            print(data)

    writer = Writer()
    writer.write("data")
