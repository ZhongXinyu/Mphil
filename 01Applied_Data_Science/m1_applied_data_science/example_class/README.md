## Problem set 4 ##

### Q1

Plot the data from data file [`q1.csv`](q1.csv). Perform k-means for a range of values of K. Evaluate the silhouette score in each case and use this to choose an optimal number of clusters (note: we will cover silhouette scores on Mon 27th Nov).

### Q2

In this question, we will perform vector quantisation on an image using k-means. Break the image [`moorelib-gray.png`](moorelib-gray.png) into 8x8 pixel squares and convert this into 64-dimension vectors. 

a. Cluster the resulting set of vectors using k-means. 
b. What do the cluster centroids look like? 
c. Can you use this for image compression (i.e. can you reconstruct the original image using only the cluster centroids)?

*Hint: read the png file using the following code*

```
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

image = np.asarray(Image.open(“moorelib-gray.png”))
plt.imshow(image)
```

### Q3 (Extension)

Implement your own k-means algorithm using just python and numpy (e.g. Lloyd’s algorithm with Forgy or Random Partition initialisation). Implement your algorithm on the data from [`q1.csv`](q1.csv). Can you get the same results as in Q1?
