import csv
import pprint


def read_portfolio(filename: str):
    result = []
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        for item in reader:
            symbol = item[0]
            count = int(item[1])
            price = float(item[2])
            result.append({"symbol": symbol, "count": count, "price": price})
    return result


if __name__ == "__main__":
    portfolio = read_portfolio("python-mastery/Data/portfolio.csv")
    pprint.pprint(portfolio)
