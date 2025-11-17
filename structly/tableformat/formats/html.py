from structly.tableformat.formatter import TableFormatter


class HTMLTableFormatter(TableFormatter):
    def headings(self, headers):
        print("<tr> " + " ".join(f"<tr>{item}</tr>" for item in headers) + " </tr>")

    def row(self, rowdata):
        print("<tr> " + " ".join(f"<td>{item}</td>" for item in rowdata) + " </tr>")


__all__ = ["HTMLTableFormatter"]
