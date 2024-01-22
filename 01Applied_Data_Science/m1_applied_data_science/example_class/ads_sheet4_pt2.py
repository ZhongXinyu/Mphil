
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from sklearn import cluster, metrics

# Load and plot data
image = np.asarray(Image.open('moorelib-gray.png'))

plt.figure()
plt.imshow(image, vmin=0, vmax=255)
plt.title('Original image')

# Change to try different compression
tile_size = 8

# Break the image up into 8x8 tiles
nx = np.floor(image.shape[0] / tile_size).astype(int)
ny = np.floor(image.shape[1] / tile_size).astype(int)

x = np.zeros((nx*ny, tile_size, tile_size))
for ii in range(nx):
    for jj in range(ny):
        n = (ii*ny + jj)
        x[n, :, :] = image[
            tile_size*ii:tile_size*(ii + 1), tile_size*jj:tile_size*(jj + 1)]

# Plot some of these
np.random.seed(11223)
ind = np.random.choice(range(x.shape[0]), 12)

fig, ax = plt.subplots(4, 3)
ax = ax.flatten()
for ii in range(len(ax)):
    ax[ii].imshow(x[ind[ii]], vmin=0, vmax=255)
    ax[ii].set_axis_off()
fig.suptitle('Sample tiles')
fig.tight_layout()

# Reshape to vectors
x = x.reshape(-1, tile_size*tile_size)

# Change to try different values of K
K = 10

kmeans = cluster.KMeans(n_clusters=K, n_init='auto')
labels = kmeans.fit_predict(x)
centers = kmeans.cluster_centers_.reshape(K, tile_size, tile_size)

# Plot the cluster centers corresponding to the figure above
fig, ax = plt.subplots(4, 3)
ax = ax.flatten()
for ii in range(len(ax)):
    ax[ii].imshow(centers[labels[ind[ii]]], vmin=0, vmax=255)
    ax[ii].set_axis_off()
fig.suptitle('Centroids for sample tiles')
fig.tight_layout()

# Plot each of the cluster centers
fig, ax = plt.subplots(4, 3)
ax = ax.flatten()
for ii in range(len(ax)):
    if ii < K:
        ax[ii].imshow(centers[ii], vmin=0, vmax=255)
    ax[ii].set_axis_off()
fig.suptitle('All centroids')
fig.tight_layout()

# Reconstruct the original image using the cluster centers
image_km = np.zeros(image.shape)
for ii in range(nx):
    for jj in range(ny):
        n = (ii*ny + jj)
        image_km[
            tile_size*ii:tile_size*(ii + 1),
            tile_size*jj:tile_size*(jj + 1)] = centers[labels][n]

plt.figure()
plt.imshow(image_km, vmin=0, vmax=255)
plt.title('Compressed image')

# Show all plots
plt.show()
