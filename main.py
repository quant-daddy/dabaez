from abc import ABC, abstractmethod
import time
from typing import Sequence
from tableformat import TextTableFormatter
import sys
import reader
import stock
import tableformat


class ColumnFormatMixin:
    formats = []

    def row(self, rowdata: Sequence[str]):
        rowdata = [(f % v) for f, v in zip(self.formats, rowdata)]
        super().row(rowdata)


class UpperHeadersMixin:
    def headings(self, headers: Sequence[str]):
        super().headings([header.upper() for header in headers])


class PortfolioFormatter(ColumnFormatMixin, UpperHeadersMixin, TextTableFormatter):
    formats = ["%s", "%d", "%0.2f"]


class redirect_stdout:
    def __init__(self, out_file) -> None:
        self.out_file = out_file

    def __enter__(self):
        self.stdout = sys.stdout
        sys.stdout = self.out_file
        return self.out_file

    def __exit__(self, ty, val, tb):
        sys.stdout = self.stdout


with redirect_stdout(open("output.txt", "w")) as file:
    portfolio = reader.read_csv_as_instances(
        "python-mastery/Data/portfolio.csv", stock.Stock
    )
    # formatter = tableformat.HTMLTableFormatter()
    tableformat.print_table(
        portfolio, ["name", "shares", "price"], tableformat.create_formatter("csv")
    )
    file.close()

# from datetime import date


# d = date(2008, 7, 5)
# print(d)
class IStream(ABC):
    @abstractmethod
    def read(self, maxbytes=None):
        pass

    @abstractmethod
    def write(self, data):
        pass


class UnixPipe(IStream):
    def read(self, maxbytes=None):
        pass

    def write(self, data):
        pass

    def lol(self):
        pass


def parse_line(line: str) -> tuple[str, str] | None:
    values = line.split("=")
    if len(values) != 2:
        return None
    [name, val] = values
    return (name, val)


pipe = UnixPipe()


def worker(x, y):
    print("About to work")
    time.sleep(5)
    print("Done")
    return x + y


def add(x, y):
    def foo():
        print(f"{x} + {y} ->{x + y}")

    return foo


def counter(value):
    def incr():
        nonlocal value
        value += 1
        return value

    def decr():
        nonlocal value
        value -= 1
        return value

    return incr, decr


if __name__ == "__main__":
    pass
    # pool = ThreadPoolExecutor()
    # worker_2 = lambda y: worker(2, y)
    # fut = pool.submit(worker_2, 3)
    # result = fut.result()
    # print(result)
    # formatter = formatter = create_formatter(
    #     "html", upper_headers=True, column_formats=["%s", "%d", "%0.2f"]
    # )
    # portfolio = reader.read_csv_as_instances(
    #     "python-mastery/Data/portfolio.csv", stock.Stock
    # )
    # print_table(portfolio, ["name", "shares", "price"], formatter)
