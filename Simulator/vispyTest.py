import prettyplotlib as ppl
import matplotlib.pyplot as plt
from prettyplotlib import brewer2mpl
import numpy as np
import string
import seaborn as sns

#green_purple = brewer2mpl.get_map('PRGn', 'diverging', 11).mpl_colormap
x = [[1,2,3],[4,5,6],[7,8,9]]
fig, ax = plt.subplots(1)

np.random.seed(10)

#ppl.pcolormesh(fig, ax, np.random.randn(10,10))
sns.heatmap(x)

# ax.set_title('transaction percentage of each good for each agent')
# xTickMarks = ['Agent'+str(i) for i in range(len(x))]
# ax.set_xticks(x+0.5)
# ax.set_yticks(x+0.5)
# xtickNames = ax.set_xticklabels( xTickMarks )
# ax.set_yticklabels( xTickMarks )
# plt.setp(xtickNames, rotation=90, fontsize=10)

plt.show()