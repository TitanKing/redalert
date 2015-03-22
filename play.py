class Test:

    def __init__(self):
        self.hoo_hoo = 'Is this a property?'

    def hello_normal(self, foo):
        print("Hello: " + self.hoo_hoo)
        print("Hello2: " + self.hello_static(12345))

    @staticmethod
    def hello_static(foo):
        return "Hello " + str(foo)

    @classmethod
    def hello_class(cls, foo):
        print("Hello " + foo)

t = Test()
t.hello_normal('World')