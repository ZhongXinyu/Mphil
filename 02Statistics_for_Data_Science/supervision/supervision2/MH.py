import numpy as np
import emcee

# define rosenbrock function
def rosenbrock(x):
    return sum(100.0*(x[1:]-x[:-1]**2.0)**2.0 + (1-x[:-1])**2.0)

# define the probability density function
def pdf_rosenbrock(x):
    return np.exp(-rosenbrock(x))

# Metropolis-Hastings algorithm
def Metropolis_Hastings(
        target_func = pdf_rosenbrock, # the target function
        initial_point = np.array([1,1]), # initial point
        N = 10000, # number of iterations
        cov_matrix = [[0.1, 0.075], [0.075,0.1]]  # covariance matrix
        ):
    # dimension of the target function
    d = len(initial_point)

    # initial point
    x = initial_point
    
    # list of accepted points
    chain = [x]

    # iteration index 
    i = 0
    
    # proposal distribution
    def gaussian(mean, cov_matrix):
        return np.random.multivariate_normal(mean, cov_matrix)

    def inv_gaussain(x, mean, cov_matrix):
        # return the probability of x given mean and cov_matrix
        return np.exp(-0.5 * (x - mean).T @ np.linalg.inv(cov_matrix) @ (x - mean)) / (2 * np.pi)**(d/2) / np.sqrt(np.linalg.det(cov_matrix))


    acceptance = 0
    
    while i < N:
        # a proposal distribution
        y = gaussian(mean = x, cov_matrix = cov_matrix)
        # compute the acceptance ratio
        a = target_func(y)/target_func(x) * inv_gaussain(x, y, cov_matrix) / inv_gaussain(y, x, cov_matrix)
        # compute the uniform random number
        u = np.random.rand()
        # accept the new point if the random number is less than the acceptance ratio
        if u < a:
            x = y
            chain.append(x)
            acceptance += 1
        else:
            chain.append(x)
        i += 1
    return chain, acceptance/N



class MetropolisHastings:
    def __init__(self, 
            target_func = pdf_rosenbrock, # the target function
            ndim = 2, # dimension of the target function
            initial_point = None, # initial point
            N = 100000, # number of iterations
            cov_matrix = None, # covariance matrix
            thinning_factor = 1 # thinning factor
            ):
        self.target_func = target_func
        
        if initial_point is None:
            self.initial_point = np.array([1]*ndim)
        else:
            self.initial_point = initial_point
        
        if cov_matrix is None:
            self.cov_matrix = np.eye(ndim)
        else:
            self.cov_matrix = cov_matrix
        
        self.N = N
        self.ndim = ndim
        self.chain = []
        self.thinning_factor = thinning_factor
    
    def gaussian(self, mean, cov_matrix):
        return np.random.multivariate_normal(mean, cov_matrix)

    def inv_gaussian(self, x, mean, cov_matrix):
        
        return np.exp(-0.5 * (x - mean).T @ np.linalg.inv(cov_matrix) @ (x - mean)) / (2 * np.pi)**(self.ndim/2) / np.sqrt(np.linalg.det(cov_matrix))

    def sample(self):
        x = self.initial_point
        self.chain = [x]
        acceptance = 0
        i = 1

        while len(self.chain) < self.N:
            y = self.gaussian(mean=x, cov_matrix=self.cov_matrix)
            a = self.target_func(y) / self.target_func(x) * self.inv_gaussian(x, y, self.cov_matrix) / self.inv_gaussian(y, x, self.cov_matrix)
            u = np.random.rand()

            if u < a:
                x = y
                acceptance += 1

            # Thinning: Only add to chain when the current iteration is a multiple of the thinning factor
            if i % self.thinning_factor == 0:
                self.chain.append(x)
            
            i += 1

        self.acceptance_rate = acceptance / i
        self.IAT = emcee.autocorr.integrated_time(self.chain, quiet = True)
        self.effective_sample_size = self.N / self.IAT
        
        return None
    
    def reset(self):
        self.chain = []
        self.acceptance_rate = None
        self.IAT = None
        self.effective_sample_size = None
        return None

    def get_chain(self):
        return self.chain
    
    def get_acceptance_rate(self):
        return self.acceptance_rate
    
    def get_IAT(self):
        return self.IAT
    
    def summary(self):
        print ("Summary for Metropolis Hastings (Zachary)")
        print ("---------")
        print ("Number of Generations: ", len(self.chain))
        print ("Dimension: ", self.ndim)
        print ("Acceptance Rate: ", self.acceptance_rate)
        print ("Integrated Autocorrelation Time: ", self.IAT)
        print ("Effective Sample Size: ", self.effective_sample_size)
        return None

