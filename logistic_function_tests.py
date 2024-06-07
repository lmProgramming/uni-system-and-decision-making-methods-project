import numpy as np
import math
import random
import matplotlib.pyplot as plt

def custom_logistic(x, mn, mx, mean):    
    m_inter = (mean-mn)/(mx-mn)
       
    return x**math.log(m_inter, 0.5) * (mx-mn) + mn

mn = 20
mx = 100
mean = 40
k = 5

mnx = (mean - mn) / (mx - mn)

x_values = np.linspace(0.001, 1, 1000)
y_values = custom_logistic(x_values, mn, mx, mean)

suma = 0
for i in range(1000):
    suma += custom_logistic(random.uniform(0., 1.), mn, mx, mean)
print(suma / 1000)

plt.plot(x_values, y_values)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Custom Logistic Function')
plt.grid(True)
plt.show()
