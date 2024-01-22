
from hmac import new
import numpy as np
import random
class datamean:
    def __init__(self, data, max_iter=10, initiation= "Forgy", num_centroids= 4, distance = "Euclidean"):
        self.data = data
        self.data_num = data.shape[0] # number of centroids
        self.dimension = data.shape[1] # dimension of the data
        self.particles = [Particle(data[i], index = i) for i in range(self.data_num)]

        self.distance = distance
        self.max_iter = max_iter
        self.initiation = initiation
        self.num_centroids= num_centroids
        self.clusters = [] # a list of Cluster Objects, will be initiated later 
        self.membership = [[ 0 for j in range(num_centroids)] for i in range(self.data_num)] # membership matrix
    
    def initiate(self) -> None:
        # initiate the centroids
        if self.initiation == "Forgy":
            # randomly select k data points as centroids
            self.clusters = [Cluster(Centroid(self.data[random.randint(0, self.data_num-1)], i))for i in range(self.num_centroids)]
        elif self.initiation == "Random Partition":
            # randomly assign each data point to a cluster
            for i in range(self.data_num):
                self.membership[i][random.randint(0,self.num_centroids-1)] = 1
            # update the clusters
            self.clusters = [Cluster(centroid= Centroid(loc = np.zeros(self.dimension))) for i in range(self.num_centroids)]
            self.update_centroids()
    
    def update_membership(self):
        # update the membership matrix
        for i in range(self.data_num):
            distance_list = [self.particles[i].distance_from(self.clusters[j].centroid, method = self.distance) for j in range (self.num_centroids)]
            closest_centroid_number = np.argmin(distance_list)
            self.membership[i] = [1 if k == closest_centroid_number else 0 for k in range(self.num_centroids)]
    
    def update_centroids(self):
        # update the centroids
        for i in range(self.num_centroids):
            # find the data points that belong to the ith centroid
            data_points = [self.particles[j].loc for j in range(self.data_num) if self.membership[j][i] == 1]
            # calculate the mean of the data points
            if data_points == []:
                print (f"empty cluster {i}")
                continue
            new_loc = np.mean(data_points,axis=0)
            # update the ith centroid
            self.clusters[i].centroid.update_loc(new_loc)
            self.clusters[i].particles = [self.particles for j in range(self.data_num) if self.membership[j][i] == 1]
    
    def fit(self):
        # initiate the centroids
        self.initiate()
        # fit the data
        for i in range(self.max_iter):
            self.update_membership()
            self.update_centroids()
    
    def label(self) ->list:
        # return the labels of the data points
        return [np.argmax(self.membership[i]) for i in range(self.data_num)]

    def centers(self) -> np.ndarray:
        # return the centers of the clusters
        return np.asarray([self.clusters[i].centroid.loc for i in range(self.num_centroids)])
        
class Particle:
    def __init__(self, loc: np.ndarray, index: int = 0):
        self.loc = loc
        self.index = index
    
    def distance_from(self, other:"Particle", method = "Euclidean"):
        if method == "Euclidean":
            return np.sqrt(np.sum((self.loc - other.loc)**2))
        if method == "Manhattan":
            return np.sum(np.abs(self.loc - other.loc))

class Centroid(Particle):
    def __init__(self, loc: np.array, index: int = 0):
        self.loc = loc
        self.index = index
    
    def update_loc(self, new_loc: np.array):
        self.loc = new_loc


class Cluster():
    def __init__(self, centroid: Centroid, particles:list["Particle"] = []):
        self.centroid = centroid
        self.particles = []
    
    def add_particle(self, particle: Particle):
        self.particles.append(particle)
    

    
    

    

