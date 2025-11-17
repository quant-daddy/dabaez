import logging


log = logging.getLogger(__name__)


def typedproperty(name, expected_type):
    private_name = "_" + name

    @property
    def value(self):
        return getattr(self, private_name)

    @value.setter
    def value(self, val):
        if not isinstance(val, expected_type):
            raise TypeError(f"Expected {expected_type}")
        setattr(self, private_name, val)

    return value


def String(name):
    return typedproperty(name, str)


def Integer(name):
    return typedproperty(name, int)


def Float(name):
    return typedproperty(name, float)


def test():
    try:
        1 + "2"
    except Exception as e:
        log.error(e)
        raise TypeError("not correct type") from e


if __name__ == "__main__":
    test()
