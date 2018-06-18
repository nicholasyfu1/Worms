import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=np.array([210,297])/25.4)
x = np.linspace(0,2*np.pi,100)
plt.plot(x,np.sin(x))
plt.gca().set_position([0,0.2,1,.5])
plt.show()
