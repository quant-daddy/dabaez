import csv
from typing import Sequence


class IntegerWeak:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, cls):
        print("__get__", instance)
        return instance.__dict__[self.name]


class Integer:
    def __init__(self, name) -> None:
        self.name = name

    def __get__(self, instance, cls):
        print("__get__", instance)
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError("Expected an integer")
        instance.__dict__[self.name] = value


class Stock:
    a = Integer("a")
    b = IntegerWeak("b")
    _types = (str, int, float)

    # __slots__ = ("name", "_shares", "_price")

    def __init__(self, name: str, shares: int, price: float) -> None:
        self.name = name
        self.price = price
        self.shares = shares

    @property
    def shares(self):
        return self._shares

    @shares.setter
    def shares(self, value):
        if not isinstance(value, self._types[1]):
            raise TypeError("shares must be an", self._types[1])
        elif value < 0:
            raise ValueError("shares must be non negative")
        else:
            self._shares = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not (isinstance(value, self._types[2])):
            raise TypeError("Price must be a ", self._types[2])
        elif value <= 0:
            raise ValueError("Price must be positive")
        else:
            self._price = value

    @classmethod
    def from_row(cls, row):
        values = [func(val) for func, val in zip(cls._types, row)]
        return cls(*values)  # type: ignore

    @property
    def cost(self):
        return self.shares * self.price

    def sell(self, shares: int):
        if self.shares < shares:
            raise ValueError(f"{shares} shares not available to sell")
        self.shares -= shares

    def __str__(self):
        return f"{self.name},{self.price},{self.shares}"

    def __repr__(self):
        return f"Stock(name={self.name},price={self.price},shares={self.shares})"

    def __eq__(self, v):
        return isinstance(v, Stock) and (
            (self.shares, self.price, self.name) == (v.shares, v.price, v.name)
        )


def read_portfolio(filename: str):
    with open(filename) as f:
        result = []
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            result.append(Stock.from_row(row))
            # result.append(Stock(row[0], int(row[1]), float(row[2])))
        return result


def print_portfolio(headers: Sequence[str], portfolio: Sequence[Stock]):
    print("".join(["%10s " for _ in headers]) % (tuple(headers)))
    print(" ".join(["-" * 10 for _ in headers]))
    for stock in portfolio:
        print(" ".join([f"{getattr(stock, attr):>10s}" for attr in headers]))
        # print(f"{getattr(stock, 'name'):>10s} {stock.quantity:10d} {stock.price:10.2f}")
