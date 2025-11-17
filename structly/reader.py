from abc import ABC, abstractmethod
import csv
import logging
import pprint
from typing import Any


log = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARN)


def csv_as_dicts(lines, types, *, headers=None):
    """
    Read CSV data into a list of dictionaries with optional type conversion
    """
    return convert_csv(
        lines,
        lambda headers, row: {
            name: func(val) for name, func, val in zip(headers, types, row)
        },
        headers=headers,
    )


def csv_as_instances(lines, cls, *, headers=None):
    """
    Read CSV data into a list of instances
    """
    return convert_csv(lines, lambda headers, row: cls.from_row(row), headers=headers)


def convert_csv(lines, row_mapper, *, headers=None):
    """
    Read CSV data into a list of instances
    """
    rows = csv.reader(lines)
    if headers is None:
        headers = next(rows)
    results = []
    for idx, row in enumerate(rows):
        try:
            results.append(row_mapper(headers, row))
        except Exception as e:
            log.warning(f"Row {idx}:Bad row {row}")
            log.debug("Row %d: Reason: %s" % (idx, e))
    return results


def read_csv_as_dicts(filename, types):
    lines = open(filename)
    records = csv_as_dicts(lines, types)
    return records


def read_csv_as_instances(filename, cls):
    """
    Read CSV data into a list of instances
    """
    lines = open(filename)
    records = csv_as_instances(lines, cls)
    return records


class CSVParser(ABC):
    def parse(self, filename):
        result = []
        with open(filename, "r") as file:
            rows = csv.reader(file)
            header = next(rows)
            for row in rows:
                result.append(self.make_record(header, row))
        return result

    @abstractmethod
    def make_record(self, headers, row) -> Any:
        pass


class DictCSVParser(CSVParser):
    def __init__(self, types):
        self.types = types

    def make_record(self, headers, row):
        return {k: func(v) for k, func, v in zip(headers, self.types, row)}


class InstanceCSVParser(CSVParser):
    def __init__(self, cls: Any):
        self.cls = cls

    def make_record(self, headers, row):
        return self.cls.from_row(row)


def make_dict(headers, row):
    return dict(zip(headers, row))


if __name__ == "__main__":
    lines = open("python-mastery/Data/missing.csv")
    pprint.pprint(csv_as_dicts(lines, [str, int, float]))

__all__ = ["read_csv_as_instances", "read_csv_as_dicts"]
