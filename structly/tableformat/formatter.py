from abc import ABC, abstractmethod
from typing import Any, Literal, Sequence


class TableFormatter(ABC):
    @abstractmethod
    def headings(self, headers):
        pass

    @abstractmethod
    def row(self, rowdata):
        pass


def print_table(
    items: Sequence[Any], headers: Sequence[str], formatter: TableFormatter
):
    if not isinstance(formatter, TableFormatter):
        raise TypeError("formatter must be of type TableFormatter")
    formatter.headings(headers)
    # print("".join(["%10s " for _ in headers]) % (tuple(headers)))
    # print(" ".join(["-" * 10 for _ in headers]))
    for item in items:
        rowdata = [getattr(item, attr) for attr in headers]
        formatter.row(rowdata)
        # print(" ".join([f"{str(getattr(item, attr)):>10s}" for attr in headers]))
        # print(f"{getattr(stock, 'name'):>10s} {stock.quantity:10d} {stock.price:10.2f}")


from .formats import *


def create_formatter(
    format: Literal["csv", "html", "text"], upper_headers=False, column_formats=None
):
    class UpperHeadersMixin:
        def headings(self, headers: Sequence[str]):
            super().headings(
                [header.upper() if upper_headers else header for header in headers]
            )

    class ColumnFormatMixin:
        formats = column_formats or None

        def row(self, rowdata: Sequence[str]):
            rowdata = (
                [(f % v) for f, v in zip(self.formats, rowdata)]
                if self.formats
                else rowdata
            )
            super().row(rowdata)

    match format:
        case "csv":
            BaseFormatter = CSVTableFormatter
        case "html":
            BaseFormatter = HTMLTableFormatter
        case "text":
            BaseFormatter = TextTableFormatter
        case _:
            raise ValueError(f"Unknown format {format}")

    class Formatter(ColumnFormatMixin, UpperHeadersMixin, BaseFormatter):
        pass

    return Formatter()


__all__ = ["TableFormatter", "print_table", "create_formatter"]
