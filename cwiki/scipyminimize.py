from scipy.optimize import minimize
import numpy as np

def f_1(x1, x2):
    return (x1 - 1) * (x2 - 1) * x1 * x2

def f(x):
    return f_1(x[0], x[1])

def P_1(x1, x2):
    return max(0, (x1 - 1)**2 + x2**2 - 1)

def P(x):
    return P_1(x[0], x[1])

xo = np.array([1.92457742, 0.43302863])

cons = {'type': 'ineq', 'fun': P}

res = xo
print(f'Initial point {res}, value {f(res)}')

i = 1
epsilon = 0.001
prev_point = res
rho = 2

while True:
    current = lambda x: f(x) + rho * P(x) ** 2

    res = minimize(current, xo).x

    print(f'Iteration {i}, point {res}, value {f(res)}, distance {np.linalg.norm(res - prev_point)}')

    distance = np.linalg.norm(res - prev_point)
    if distance < epsilon:
        break

    prev_point = res
    rho *= 2
    i += 1

print("Minimum znajduje się w punkcie:", res)
print("Wartość funkcji celu w tym punkcie:", f(res))
