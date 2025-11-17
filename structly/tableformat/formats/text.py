from typing import Sequence
from structly.tableformat.formatter import TableFormatter


class TextTableFormatter(TableFormatter):
    def headings(self, headers: Sequence[str]):
        print(" ".join("%10s" % header for header in headers))
        print(("-" * 10 + " ") * len(headers))

    def row(self, rowdata: Sequence[str]):
        print(" ".join("%10s" % str(item) for item in rowdata))


__all__ = ["TextTableFormatter"]
