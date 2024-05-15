import numpy as np

def f(x1, x2):
    return (x1 - 1) * (x2 - 1) * x1 * x2

def P(x1, x2):
    return max(0, (x1 - 1)**2 + x2**2 - 1)

def grad_f(x1, x2):
    df_dx1 = (x2 - 1) * x2 * (2 * x1 - 1)
    df_dx2 = (x1 - 1) * x1 * (2 * x2 - 1)
    return np.array([df_dx1, df_dx2])

def grad_P(x1, x2):
    if (x1 - 1)**2 + x2**2 > 1:
        dp_dx1 = 2 * (x1 - 1)
        dp_dx2 = 2 * x2
        return np.array([dp_dx1, dp_dx2])
    else:
        return np.array([0, 0])

def grad_F(x1, x2, rho):
    return grad_f(x1, x2) + rho * grad_P(x1, x2)

alpha = 0.005  
max_iter = 20  
tolerance = 0.02

x1_range = np.linspace(-1, 2, 400)
x2_range = np.linspace(-1, 2, 400)
x1, x2 = np.meshgrid(x1_range, x2_range)


alpha = 0.1
max_iter = 100 
tolerance = 0.001 
rho = 1

x = np.array([1.6, -0.1])

while True:
    for _ in range(max_iter):
        grad = grad_F(x[0], x[1], rho)
        new_x = x - alpha * grad
        print(f"Gradient: {grad}")
        print(f"X: {new_x}")
        print(np.linalg.norm(new_x - x))
        print(_ + 1)
        
        if np.linalg.norm(new_x - x) < tolerance:
            print(_ + 1)
            break

        x = new_x
        
    rho *= 2    
        
    print(f"Wartość: {f(x[0], x[1])}, x = {x}")
    input()    
    