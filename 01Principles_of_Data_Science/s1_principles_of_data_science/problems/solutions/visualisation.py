import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# read the dataset
df = pd.read_pickle("../s1_principles_of_data_science/datasets/ps1.pkl")

# Part A
# make a pair plot using seaborn
sns.pairplot( df )
plt.savefig("figs/s1_pairplot.pdf")
sns.pairplot( df, kind='kde')
plt.savefig("figs/s1_pairplot_kde.pdf")
sns.pairplot( df, kind='hist')
plt.savefig("figs/s1_pairplot_hist.pdf")

# Part B
# make a publication style plot
plt.style.use('code/mphil.mplstyle')
fig, ax = plt.subplots()
x, y = df['vx'], df['vz']
sns.scatterplot(x=x, y=y, s=5, color="0.15")
sns.histplot(x=x,y=y, bins=25, pthresh=0.1, cmap="mako", alpha=0.9)
sns.kdeplot(x=x, y=y, levels=5, color='w', linewidths=1)
ax.set_xlabel('Variable A')
ax.set_ylabel('Variable B')
fig.savefig("figs/s1_pubplot.pdf")

# Part C
print( df.corr() )
print( df.cov() )
print( df.corr().to_latex() )
print( df.cov().to_latex() )

plt.show()
