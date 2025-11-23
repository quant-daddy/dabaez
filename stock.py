from structly.structure import Structure
from structly.validate import PositiveFloat, PositiveInteger, String


class Stock(Structure):
    name = String()
    shares = PositiveInteger()
    price = PositiveFloat()

    @property
    def cost(self):
        return self.shares * self.price

    def sell(self, shares: PositiveInteger):
        self.shares -= shares


if __name__ == "__main__":
    from structly import read_csv_as_instances, create_formatter, print_table

    portfolio = read_csv_as_instances("python-mastery/Data/portfolio.csv", Stock)
    formatter = create_formatter("text")
    print_table(portfolio, ["name", "shares", "price"], formatter)
