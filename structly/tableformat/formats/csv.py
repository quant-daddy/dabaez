from typing import Sequence
from structly.tableformat.formatter import TableFormatter


class CSVTableFormatter(TableFormatter):
    def headings(self, headers):
        print(",".join(header for header in headers))

    def row(self, rowdata: Sequence[str]):
        print(",".join([str(item) for item in rowdata]))


__all__ = ["CSVTableFormatter"]
