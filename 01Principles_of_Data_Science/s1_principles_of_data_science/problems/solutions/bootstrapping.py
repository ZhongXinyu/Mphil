import numpy as np
np.random.seed(1)
from resample import jackknife, bootstrap

x = np.random.normal(1, 5, size=200)

# biased standard deviation
sdev = np.std( x )

# unbiased standard deviation
sdevc = np.std( x, ddof=1 )

# jackknife 
jk_bias = jackknife.bias( np.std, x )
jk_std = jackknife.bias_corrected( np.std, x )

# bootstrap
bt_bias = bootstrap.bias( np.std, x, size=5000 )
bt_std = bootstrap.bias_corrected( np.std, x, size=5000 )

print('Estimate of variance without Bessel Correction: ', sdev )
print('Estimate of variance with Bessel Correction:    ', sdevc )
print('Estiamate of bias:')
print('   jackknife:', jk_bias )
print('   bootstrap:', bt_bias )
print('Bias-corrected estimate:')
print('   jackknife:', jk_std )
print('   bootstrap:', bt_std )

