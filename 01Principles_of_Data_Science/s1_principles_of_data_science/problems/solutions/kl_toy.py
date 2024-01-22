import numpy as np
from scipy.stats import truncnorm as tnorm
from numba_stats import uniform, truncnorm
import matplotlib.pyplot as plt
plt.style.use('code/mphil.mplstyle')
from iminuit import Minuit, cost
from tqdm import tqdm

ctM = 1
ctS = 0.05
f = 0.1

# going to tighten the range from [0.9, 1]
# and work out that fraction instead
xrange = [-1, 1]

def bmod(x):
    return uniform.pdf(x, xrange[0], xrange[1]-xrange[0])

def smod(x, mu=ctM, sg=ctS):
    return truncnorm.pdf(x, *xrange, mu, sg)

def tmod(x, f=f, mu=ctM, sg=ctS):
    return f*smod(x, mu, sg) + (1-f)*bmod(x)

def tplot(x, N, f, mu, sg):
    return N*f*smod(x, mu, sg) + N*(1-f)*bmod(x)

def tdens(x, N, f, mu, sg):
    return N, tplot(x,N,f,mu,sg) 

def generate(f, size):

    Ns = f*size
    Nb = (1-f)*size

    Ns = np.random.poisson(Ns)
    Nb = np.random.poisson(Nb)
    
    lowp = (xrange[0]-ctM)/ctS
    uppp = (xrange[1]-ctM)/ctS
    sig = tnorm(lowp, uppp, ctM, ctS).rvs(size=Ns)
    bkg = np.random.uniform(xrange[0], xrange[1], size=Nb)

    return np.concatenate( [sig, bkg] )

def fit( dset ):

    nll = cost.ExtendedUnbinnedNLL( dset, tdens )
    mi = Minuit(nll, N=5000, f=0, mu=ctM, sg=ctS)
    mi.limits['N'] = (3000,8000)
    mi.limits['f'] = (-0.5, 0.5)
    mi.fixed['mu','sg'] = True
    mi.migrad()
    mi.hesse()
    return mi

def fit_both_hyp( dset, verbose=False ):

    nll = cost.ExtendedUnbinnedNLL( dset, tdens )
    mi = Minuit(nll, N=5000, f=0, mu=ctM, sg=ctS)
    mi.limits['N'] = (3000,8000)
    mi.limits['f'] = (-0.5,0.5)
    mi.fixed['mu','sg'] = True
    mi.migrad()
    mi.hesse()
    snll = mi.fval
    
    if verbose:
        print(mi)

    mi.values['f'] = 0
    mi.fixed['f'] = True
    mi.migrad()
    mi.hesse()
    bnll = mi.fval
    
    if verbose:
        print(mi)

    return bnll - snll


def plot( dset, N, f, mu, sg ):

    fig, ax = plt.subplots()

    nh, xe = np.histogram( dset, bins=50, range=xrange )
    cx = 0.5*(xe[1:]+xe[:-1])
    ax.errorbar( cx, nh, nh**0.5, fmt='ko' )
    bw = xe[1]-xe[0]

    x = np.linspace(*xrange, 400, endpoint=False)
    ax.plot(x, N*f*bw*smod(x, mu, sg))
    ax.plot(x, N*(1-f)*bw*bmod(x))
    ax.plot(x, bw*tplot(x, N, f, mu, sg) )

def generate_test_stat( f, ntoys=1000, size=5000 ):
    
    T_vals = []
    for i in tqdm(range(ntoys)):
        dset = generate(f, size)
        T = fit_both_hyp( dset )
        T_vals.append( T )
    return T_vals

# test normal-stats
dset = generate(f, 5000)
mi = fit( dset )
plot( dset, *mi.values )
dset = np.asarray(dset)
np.save( '../s1_principles_of_data_science/datasets/kaon.npy', dset)
print(mi)

fig, ax = plt.subplots()

T_H0 = generate_test_stat( f=0, ntoys=5000 )
ax.hist( T_H0, bins=50, density=True, histtype='step', label='$f=0$')
exp_H0 = np.median( T_H0 )

fpoints = np.linspace(0, 0.02, 21)[1:]
T_H1s = []
CL_sbs = [0.5]
CL_ss = [1] 
for i, fval in enumerate(fpoints):
    T_H1 = np.asarray( generate_test_stat( f=fval, ntoys=5000 ) )
    T_H1s.append( T_H1 )
    if i%3==0:
        ax.hist( T_H1, bins=50, density=True, histtype='step', label=f'$f={fval:5.3f}$')

    CL_sb = len( T_H1[ T_H1 <= exp_H0 ] ) / len( T_H1 )

    CL_sbs.append( CL_sb )
    CL_ss.append( CL_sb / 0.5 )

T_H0 = np.asarray(T_H0)
T_H1s = np.asarray(T_H1s)

ax.set_yscale('log')
ax.set_xlabel('$T$')
ax.set_ylabel('Probability')
ax.legend()
fig.savefig('figs/kaon_test_stat.pdf')

fpoints = [0] + list(fpoints)
from scipy.interpolate import interp1d
func_clsb = interp1d( CL_sbs, fpoints )
func_cls = interp1d( CL_ss, fpoints )

f_clsb = func_clsb(0.1)
f_cls = func_cls(0.1)

fig, ax = plt.subplots()
ax.plot( fpoints, CL_sbs, c='r', label='Expected $CL_{sb}$' )
ax.plot( fpoints, CL_ss , c='b', label='Expected $CL_{s}$'  )
ax.plot( fpoints, np.full_like(fpoints, 0.5), c='g', label='Expected $CL_{b}$')
ax.plot( [0, f_cls], [0.1,0.1], 'b:' )
ax.plot( [f_cls, f_cls], [0,0.1], 'b:' )
ax.plot( [0, f_clsb], [0.1,0.1], 'r--' )
ax.plot( [f_clsb, f_clsb], [0,0.1], 'r--' )
ax.set_xlabel('$f$')
ax.set_ylabel('1-CL')
ax.legend()
ax.autoscale(axis='x', enable=True, tight=True)
fig.savefig('figs/kaon_limit.pdf')

print('CLsb: @90%', f_clsb )
print('CLs: @90%', f_cls )
plt.show()



