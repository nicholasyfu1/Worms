import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.patches as mpatches

# create the figure and the axis in one shot
fig, ax = plt.subplots(1,figsize=(6,6))

art = mpatches.Circle([0,0], radius = 1, color = 'r')
#use add_patch instead, it's more clear what you are doing
ax.add_patch(art)

art = mpatches.Circle([0,0], radius = 0.1, color = 'b')
ax.add_patch(art)

print ax.patches

#set the limit of the axes to -3,3 both on x and y
ax.set_xlim(-3,3)
ax.set_ylim(-3,3)

plt.show()
