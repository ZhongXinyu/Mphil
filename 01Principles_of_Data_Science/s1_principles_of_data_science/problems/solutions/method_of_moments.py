## Solution to Problem Sheet 3 Question 1
## once again more optimal solutions will be available

import numpy as np
np.random.seed(210187)
from scipy.optimize import brute, minimize
from scipy.integrate import quad
from scipy.stats import moment
import matplotlib.pyplot as plt
plt.style.use('code/mphil.mplstyle')
from jacobi import propagate
from iminuit import cost, Minuit
import sys
sys.path.append('$PWD/code')
from accept_reject import accept_reject_1d, check_ok_plot
from tabulate import tabulate

if __name__=="__main__":

    xrange = [-0.95,0.95]
    alpha = 0.5
    beta = 0.5
    
    def dk(k):
        return (xrange[1]**k - xrange[0]**k)/k

    N = 1/( dk(1) + alpha*dk(2) + beta*dk(3) )

    func = lambda x: N*(1 + alpha*x + beta*x**2)
    
    # run the accept-reject
    dset = accept_reject_1d( func, xrange=xrange, size=2000 )
    check_ok_plot( func, xrange, dset, bins=40, save=f'figs/mom_gen.pdf' )
    dset = np.asarray(dset)
    np.save('../s1_principles_of_data_science/datasets/mom_data.npy', dset)

    # MoM estimate
    m1_hat = moment(dset, moment=1, center=0)
    m2_hat = moment(dset, moment=2, center=0)

    def alpha(m1, m2):
        numerator = (m1*dk(3) - dk(4))*(m2*dk(1)-dk(3)) - (m1*dk(1)-dk(2))*(m2*dk(3)-dk(5))
        denominator = (m1*dk(2) - dk(3))*(m2*dk(3)-dk(5)) - (m1*dk(3)-dk(4))*(m2*dk(2)-dk(4))
        return numerator / denominator

    def beta(m1, m2):
        numerator = (m1*dk(1) - dk(2))*(m2*dk(2)-dk(4)) - (m1*dk(2)-dk(3))*(m2*dk(1)-dk(3))
        denominator = (m1*dk(2) - dk(3))*(m2*dk(3)-dk(5)) - (m1*dk(3)-dk(4))*(m2*dk(2)-dk(4))
        return numerator / denominator
    
    alpha_hat = alpha(m1_hat, m2_hat)
    beta_hat = beta(m1_hat, m2_hat)
   
    N = len(dset)
    cov11 = 1/(N*(N-1)) * np.sum( (dset-m1_hat) * (dset-m1_hat) )
    cov22 = 1/(N*(N-1)) * np.sum( (dset**2-m2_hat) * (dset**2-m2_hat) )
    cov12 = 1/(N*(N-1)) * np.sum( (dset-m1_hat) * (dset**2-m2_hat) )

    cov_hat = np.array( [[cov11,cov12],[cov12,cov22]] )

    # propagate to parameter estimates

    transform = lambda p: np.array( [ alpha(*p), beta(*p) ] )

    mom, mom_cov = propagate( transform, [m1_hat, m2_hat], cov_hat )
    
    # Now some kind of MLE

    def density(x, alpha, beta):
        N = 1/( dk(1) + alpha*dk(2) + beta*dk(3) )
        return N*(1 + alpha*x + beta*x**2)
    
    nll = cost.UnbinnedNLL(dset, density)
    mi = Minuit( nll, alpha=0.5, beta=0.5 )
    mi.migrad()
    mi.hesse()

    print("---- METHOD OF MOMENTS ----")
    print(tabulate(zip(['alpha','beta'], mom, np.diag(mom_cov)**0.5), headers=['Parameter','Value','Error']))
    print("---- MAXIMUM LIKELIHOOD ---")
    print(tabulate(zip(['alpha','beta'], list(mi.values), list(mi.errors)), headers=['Parameter','Value','Error']))

    plt.show()




