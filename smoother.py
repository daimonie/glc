import numpy as np 
from scipy.optimize import minimize
from smoother import *


#Smooth and bootstrap data
proposed_function = lambda x, jj: x[0] + x[1]*jj + x[2] * jj**2 + x[3] * np.exp( x[4] * jj) + x[4] * jj**3
    
def lsqe(x, coupling, critical):
    global proposed_function
    proposed_values = proposed_function(x, coupling)
    
    error = critical - proposed_values
    squares = np.square(error).sum()
    
    last = critical.shape[0]-1
    
    squares += 10*(critical[0] - proposed_values[0])**2
    squares += 10*(critical[last] - proposed_values[last])**2
    
    return squares
def smooth_bootstrap(coup, crit, points):  
    global proposed_function  
    optimizer = minimize( lsqe, [np.average(crit), 0.0, 0.0, 1.0, 0.1, 0.0], args=(np.array(coup),crit),
        jac=False, method='L-BFGS-B', options={'disp': False}, tol = 1e-6)
        
    x = optimizer.x 
    smooth_coup = np.linspace( np.min(coup), np.max(coup), points);
    smooth_crit = proposed_function(x, smooth_coup)
    
    return smooth_coup, smooth_crit