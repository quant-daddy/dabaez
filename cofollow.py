from collections import deque
from functools import wraps
from typing import Any, Callable, Generator
import time


def consumer(func: Callable[..., Generator[Any, Any, Any]]):
    @wraps(func)
    def wrapper(*args, **kwargs):
        f = func(*args, **kwargs)
        f.send(None)
        return f

    return wrapper


def follow(filename, target: Generator[Any, str, Any]):
    """
    Tails a file and sends line to the target
    """
    f = open(filename, mode="r")
    while True:
        line = f.readline()
        if line == "":
            time.sleep(0.1)
            continue
        target.send(line)


@consumer
def printer():
    """
    Corountine that prints inputs sent to it
    """
    while True:
        try:
            line = yield
            if line:
                print(line)
        except Exception as e:
            print("ERROR: %r" % e)


def countdown(n):
    while n > 0:
        yield
        print(f"T minus {n}")
        n = n - 1


def countup(n):
    x = 0
    while x < n:
        yield
        print(f"Up we go {x}")
        x = x + 1


if __name__ == "__main__":
    tasks = deque([countdown(10), countdown(5), countup(5)])
    while tasks:
        task = tasks.popleft()
        try:
            task.send(None)
            print("appending task back")
            tasks.append(task)
        except StopIteration:
            pass
