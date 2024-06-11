import numpy as np
import math
import matplotlib.pyplot as plt
import random

def custom_logistic(x, minimum, maximum, mean):    
    m_inter = (mean-minimum)/(maximum-minimum)
       
    return x**math.log(m_inter, 0.5) * (maximum-minimum) + minimum

minimum = 20
maximum = 100
mean = 40

mnx: float = (mean - minimum) / (maximum - minimum)

x_values = np.linspace(0.001, 1, 1000)
y_values = custom_logistic(x_values, minimum, maximum, mean)

print(sum(custom_logistic(random.uniform(0., 1.), minimum, maximum, mean) for _ in range(100000)) / 100000)

plt.plot(x_values, y_values)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Custom Logistic Function')
plt.grid(True)
plt.show()