import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from MyKmean import Kmean as MyKmean
from sklearn.cluster import KMeans


data = np.genfromtxt("q1.csv", delimiter=',')
n = 11

Mykmean = MyKmean(data, num_centroids = n, max_iter= 10, distance = "Manhattan", initiation= "Forgy")
Myk_random = MyKmean(data, num_centroids = n, max_iter= 10, distance = "Manhattan", initiation= "Random Partition")
SkKmean = KMeans(n_clusters=n, random_state=0, n_init = n, init = "random").fit(data)

Mykmean.fit()
Myk_random.fit()

label_forgy = Mykmean.label()
label_random = Myk_random.label()
label_sk = SkKmean.labels_

centers_forgy = Mykmean.centers()
centers_random = Myk_random.centers()
centers_sk = SkKmean.cluster_centers_

for i in range(n):
    print (f"cluster {i} has {label_random.count(i)} data points")

# plot the data points

fig, axs = plt.subplots(1, 3, figsize=(10, 4))

axs[0].scatter(data[:,0],data[:,1],c = label_forgy)
axs[0].scatter(centers_forgy[:,0], centers_forgy[:,1],c = "red")
axs[0].set_title("MyKmean Forgy")
axs[1].scatter(data[:,0],data[:,1],c = label_random)
axs[1].scatter(centers_random[:,0],centers_random[:,1],c = "red")
axs[1].set_title("MyKmean Random Partition")
axs[2].scatter(data[:,0],data[:,1],c = label_sk)
axs[2].scatter(centers_sk[:,0],centers_sk[:,1],c = "red")
axs[2].set_title("sklearn Kmean")

plt.show()