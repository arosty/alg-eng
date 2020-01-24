from test import tester
from smac.facade.func_facade import fmin_smac

x, cost, sth = fmin_smac(
    func=tester,
    x = 5,
    bounds = [(-10,10)],
    maxfun = 20,
    rng = 3)
print('---')
print(x)
print(cost)
print(sth)
print('---')