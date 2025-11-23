from typing import Any, Generator
from cofollow import consumer
from structly.structure import Structure
from structly.validate import Float, Integer, String


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
def match(pattern: str, target: Generator[Any, str, Any]):
    """
    coroutine that takes input and filters it by patterns and sends the result to target
    """
    print(f"looking for {pattern}")
    while True:
        line = yield
        if pattern in line:
            target.send(line)


if __name__ == "__main__":
    ...
    # from follow import follow
    # import csv
    # from structly.tableformat import create_formatter, print_table

    # formatter = create_formatter("text")

    # lines = follow("python-mastery/Data/stocklog.csv")
    # rows = csv.reader(lines)
    # records = (Ticker.from_row(row) for row in rows)
    # negatives = (rec for rec in records if rec.change < 0.0)
    # print_table(negatives, ["name", "price", "change"], formatter)
