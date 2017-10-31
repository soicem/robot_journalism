import random

from example_code.coroutine.clockdeco_param import clock

@clock('{name}({args}) dt={elapsed:0.3f}s')
def start():
    list = []
    for _ in range(60):
        list.append(random.randint(0, 10000 - 1))
        print(list)
    return list
print(start())