class Descriptor:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, cls):
        print("%s:__get__" % self.name)

    def __set__(self, instance, value):
        print("%s:__set__ %s" % (self.name, value))

    def __delete__(self, instance):
        print("%s:__delete__" % self.name)


class Foo:
    a = Descriptor("a")
    b = Descriptor("b")
    c = Descriptor("c")


class Base1:
    def spam(self):
        print("Base1.spam")


class Base2:
    def spam(self):
        print("Base2.spam")


class X(Base1):
    def spam(self):
        print("X.spam")
        super().spam()


class Y(Base1):
    def span(self):
        print("Y.spam")
        super().spam()


class Z(X, Y):
    def spam(self):
        print("Z.spam")
        super().spam()
