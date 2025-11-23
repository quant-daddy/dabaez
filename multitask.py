from collections import deque

tasks = deque()


def run():
    while tasks:
        t = tasks.popleft()
        try:
            t.send(None)
            tasks.append(t)
        except StopIteration:
            print("task done")


def countdown(n):
    while n > 0:
        print("T-minus", n)
        yield
        n -= 1


def countup(n):
    x = 0
    while x < n:
        print("Up we go", x)
        yield
        x += 1


if __name__ == "__main__":
    tasks.append(countdown(10))
    tasks.append(countdown(5))
    tasks.append(countup(20))
    run()
