def portfolio_cost(filename):
    with open(filename) as f:
        cost = 0
        for line in f:
            try:
                cost += int(line.split()[1]) * float(line.split()[2])
            except ValueError:
                pass
    return cost


if __name__ == "__main__":
    print(portfolio_cost("python-mastery/Data/portfolio3.dat"))
