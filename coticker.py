from structly.structure import Structure
from structly.tableformat.formatter import create_formatter
from structly.validate import Float, Integer, String
import csv
from cofollow import consumer


class Ticker(Structure):
    name = String()
    price = Float()
    date = String()
    time = String()
    change = Float()
    open = Float()
    high = Float()
    low = Float()
    volume = Integer()


@consumer
def to_csv(target):
    """
    Coroutine that
    """

    def producer():
        while True:
            yield line

    reader = csv.reader(producer())
    while True:
        line = yield
        target.send(next(reader))


@consumer
def create_ticker(target):
    while True:
        row = yield
        target.send(Ticker.from_row(row))


@consumer
def negchange(target):
    while True:
        t: Ticker = yield
        if t.change < 0:
            target.send(t)


@consumer
def ticker(fmt, fields):
    formatter = create_formatter(fmt)
    formatter.headings(fields)
    while True:
        rec = yield
        row = [getattr(rec, name) for name in fields]
        formatter.row(row)


def closure_example():
    def incr():
        nonlocal y
        y = y + 1
        return y

    def decr():
        nonlocal y
        y = y - 1
        return y

    y = 0
    return incr, decr


if __name__ == "__main__":
    ...
    # follow(
    #     "python-mastery/Data/stocklog.csv",
    #     to_csv(create_ticker(negchange(ticker("text", ["name", "price", "change"])))),
    # )
