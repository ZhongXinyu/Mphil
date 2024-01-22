import numpy as np
np.random.seed(7)
from scipy.stats import binom
from tabulate import tabulate

theta_A = 0.32
theta_B = 0.64

# generate the coin flips
nsets = 5
nflips = 10

# array for probability per set
theta = np.random.choice( [theta_A, theta_B], size=nsets )

# array for the outcomes
data = np.array( [np.random.choice( ['H','T'], size=10, p=[th,1-th] ) for th in theta ] )

np.save('../s1_principles_of_data_science/datasets/biased_coin_flip.npy', data)

print(tabulate(data))

def post_and_exp(data, theta_T):
    res = []
    for i, vals in enumerate(data):
        nH = np.sum( vals=='H' )
        nT = np.sum( vals=='T' )
        likelihoodA = binom.pmf(nH, 10, theta_T[0])
        likelihoodB = binom.pmf(nH, 10, theta_T[1])
        likelihoodSum = likelihoodA + likelihoodB
        posteriorA = likelihoodA / likelihoodSum
        posteriorB = likelihoodB / likelihoodSum
        expectHeadsA = posteriorA*nH
        expectHeadsB = posteriorB*nH
        res.append( [i+1, posteriorA, posteriorB, expectHeadsA, expectHeadsB] )

    return res

def expec_max(data, theta_T, verbose=False):
    res = np.asarray( post_and_exp(data, theta_T) )
    exp_nHA = np.sum( res[:,3] )
    exp_nA = nflips*np.sum( res[:,1] )
    exp_nHB = np.sum( res[:,4] )
    exp_nB = nflips*np.sum( res[:,2] )

    theta_A = exp_nHA / exp_nA
    theta_B = exp_nHB / exp_nB
    
    if verbose:
        print('  '+tabulate(res, headers=['Set','PosteriorA','PosteriorB','ExpectHeadsA','ExpectHeadsB'], floatfmt='.2f' ).replace('\n','\n  ') )
        print(' ', 'thA =', theta_A, 'thB =', theta_B)

    return np.array( [theta_A, theta_B] )

# run
niter = 0
theta_T = np.array( [0.4, 0.6] )
thresh = 0.001
within_threshold = False
print('nIter | theta_A | theta_B')
print(f'{niter:5d} | {theta_T[0]:7.3f} | {theta_T[1]:7.3f}')
while not within_threshold:
    theta_T1 = expec_max(data, theta_T, verbose=True)
    
    diff = np.abs( theta_T1 - theta_T ) / theta_T
    
    theta_T = theta_T1
    niter += 1
    print(f'{niter:5d} | {theta_T[0]:7.3f} | {theta_T[1]:7.3f}')

    within_threshold = np.all( diff < thresh )
