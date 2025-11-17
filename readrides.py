from sys import intern
import collections.abc
import csv
from dataclasses import dataclass
from typing import Callable, NamedTuple


@dataclass
class RowDataclass:
    """
    Current 142173182, Peak 142203543
    """

    route: str
    date: str
    daytype: str
    rides: int


class Row:
    """
    Memory Used: Current 119067902, Peak 119098263
    """

    __slots__ = ("route", "date", "daytype", "rides")

    def __init__(self, route, date, daytype, rides) -> None:
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = int(rides)

    @classmethod
    def from_row(cls, row):
        return cls(row[0], row[1], row[2], int(row[3]))


class RowTuple(NamedTuple):
    """
    Memory Used: Current 128308806, Peak 128339167
    """

    route: str
    date: str
    daytype: str
    rides: int


def read_rides_as_dicts(filename: str):
    """
    Read the bus data as a list of tuples
    """
    records = RideData()
    with open(filename) as f:
        rows = csv.reader(f)
        next(rows)
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            # Memory Used: Current 188373598, Peak 188403959
            record = {"route": route, "date": date, "daytype": daytype, "rides": rides}
            records.append(record)
        return records


def read_rides_as_columns(filename: str):
    """
    Read the bus data as a list of tuples
    """
    routes = []
    dates = []
    daytypes = []
    rides = []
    with open(filename) as f:
        rows = csv.reader(f)
        next(rows)
        for row in rows:
            routes.append(row[0])
            dates.append(row[1])
            daytypes.append(row[2])
            rides.append(int(row[3]))
        return {"routes": routes, "dates": dates, "daytypes": daytypes, "rides": rides}


def read_csv_as_columns(filename: str, types: list[Callable]):
    with open(filename) as f:
        rows = csv.reader(f)
        header = next(rows)
        data = DataCollection(types, headers=header)
        for row in rows:
            data.append(row)
        return data


class RideData(collections.abc.Sequence):
    def __init__(self) -> None:
        self.routes = []  # Columns
        self.dates = []
        self.daytypes = []
        self.numrides = []

    def __getitem__(self, index):
        if isinstance(index, slice):
            result = RideData()
            result.routes = self.routes[index]
            result.dates = self.dates[index]
            result.daytypes = self.daytypes[index]
            result.numrides = self.numrides[index]
            return result
        else:
            return {
                "route": self.routes[index],
                "date": self.dates[index],
                "daytype": self.daytypes[index],
                "rides": self.numrides[index],
            }

    def __len__(self) -> int:
        return len(self.routes)

    def append(self, d):
        self.routes.append(d["route"])
        self.dates.append(d["date"])
        self.daytypes.append(d["daytype"])
        self.numrides.append(d["rides"])


class DataCollection(collections.abc.Sequence):
    def __init__(self, parser: list[Callable], headers: list[str]) -> None:
        self.parser = parser
        self.headers = headers
        self.data: list[list[str]] = [[] for _ in headers]

    def __getitem__(self, index):
        if isinstance(index, slice):
            result = DataCollection(self.parser, self.headers)
            result.data = [self.data[i][index] for i, _ in enumerate(self.headers)]
            return result
        else:
            return {key: val[index] for key, val in zip(self.headers, self.data)}

    def __len__(self) -> int:
        return len(self.data)

    def append(self, d: list[str]):
        for idx, (func, val) in enumerate(zip(self.parser, d)):
            self.data[idx].append(func(val))


if __name__ == "__main__":
    import tracemalloc

    tracemalloc.start()
    # rows = read_rides_as_dicts("python-mastery/Data/ctabus.csv")
    # rows = read_rides_as_columns("python-mastery/Data/ctabus.csv")
    rows = read_csv_as_columns(
        "python-mastery/Data/ctabus.csv", types=[intern, str, str, int]
    )
    print("Memory Used: Current %d, Peak %d" % tracemalloc.get_traced_memory())
