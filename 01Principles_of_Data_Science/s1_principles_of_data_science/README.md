# S1: Principles of Data Science

Welcome to the **Principles of Data Science** gitlab project.
This project contains various example scripts, modules and jupyter notebooks used in the lectures.
I will also store some example datasets here. 

### Conda environment

There is a `conda` environment file which will setup the various packages and libraries that I make use of in my code snippets.
You can create a `conda` environment from this file with e.g.

```bash
conda env create -n mphil --file environment.yml
```

Note you may want to give your environment a different name to `mphil`.
Make this environment active with

```bash
conda activate mphil
```

### `matplotlib` style

You are free to make your plots however you want.
You should remember that for publication quality plots it's really important they are easy to read.
This means having sensible colour schemes (preferably colour-blind-safe), clear and informative labels, suitable font sizes, etc.
I make extensive use of `matplotlib` and to that end also use my own `matplotlib` style file which is saved in `mphil.mplstlye`.
You can then load that style file at the top of any script that uses `matplotlib` with e.g.

```python
import matplotlib.pyplot as plt
plt.style.use('mphil.mplstyle')
```

You are free to make your own style file based on this one or just make custom changes in each script as you need them.

