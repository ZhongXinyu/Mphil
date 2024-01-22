import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches

fig, ax = plt.subplots()

rat = 6.4/4.8

xaxis = patches.FancyArrowPatch( (0,0), (0,1), arrowstyle="->" )
ax.add_artist(xaxis)

ax.annotate(None, xy=(0,0), xytext=(1,0), arrowprops=dict(arrowstyle="->"))

# hl=0.03
# hw=0.03
# ax.arrow(0, 0, 1, 0, lw=0.5, fc='k', head_length=hl, length_includes_head=True, head_width=hw)
# ax.arrow(0, 0, 0, 1, lw=0.5, fc='k', head_length=hl*rat, length_includes_head=True, head_width=hw/rat)


ax.set_axis_off()

fig.tight_layout()
plt.show()
