
import numpy as np
import matplotlib.pyplot as plt
from sklearn import cluster, metrics

# Load and plot data
x = np.loadtxt('q1.csv', delimiter=',')

plt.figure()
plt.plot(x[:, 0], x[:, 1], 'o', ms=5)

# Standardise the data
x = (x - np.tile(np.mean(x, axis=0), x.shape[0]).reshape(x.shape))
x = x / np.tile(np.std(x, axis=0), x.shape[0]).reshape(x.shape)

plt.figure()
plt.plot(x[:, 0], x[:, 1], 'o', ms=5)

# Calculate silhouette scores for each value of K
Ks = list(range(2, 11))
silhouette_scores = []

for k in Ks:
    kmeans = cluster.KMeans(n_clusters=k, n_init='auto')
    labels = kmeans.fit_predict(x)
    silhouette_scores.append(metrics.silhouette_score(x, labels))

plt.figure()
plt.plot(Ks, silhouette_scores)
plt.xlabel('K, number of clusters')
plt.ylabel('Silhouette score')
plt.ylim([0.0, 0.8])

# Plot again with the optimal number of clusters
kmeans = cluster.KMeans(n_clusters=4, n_init='auto')
plt.figure()
plt.scatter(x[:,0], x[:,1], c=kmeans.fit_predict(x))
plt.scatter(
    kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1], marker='x')

# Show all plots
plt.show()
