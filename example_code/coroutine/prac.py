from functools import wraps

class OnlyAdmin(object):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        name = kwargs.get('name').upper()
        self.func(name)

@OnlyAdmin
def greet(name):
    print("Hello {}".format(name))

greet(name='Eunwoo')