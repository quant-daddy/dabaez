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
