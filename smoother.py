import numpy as np 
from scipy.optimize import minimize
from smoother import *
from matplotlib import cm
import matplotlib.pyplot as plt


#Smooth and bootstrap data
def proposed_function(x, jj):
    value = jj*0
    for i in range(x.shape[0]):
        value += x[i] * jj**i
    return value
def lsqe(x, coupling, critical):
    proposed_values = proposed_function(x, coupling)
    
    error = critical - proposed_values
    squares = np.square(error).sum()
    
    last = critical.shape[0]-1
    
    squares += 10*(critical[0] - proposed_values[0])**2
    squares += 10*(critical[last] - proposed_values[last])**2
     
    
    return squares
def smooth_bootstrap(coup, crit, points):  
    optimizer = minimize( lsqe, [np.average(crit), 0.0, 1.0, 1.0, 0.0, 0.0, 0.0], args=(np.array(coup),crit),
        jac=False, method='L-BFGS-B', options={'disp': False}, tol = 1e-6)
        
    x = optimizer.x 
    smooth_coup = np.linspace( np.min(coup), np.max(coup), points);
    smooth_crit = proposed_function(x, smooth_coup)
    
    return smooth_coup, smooth_crit
    
def smooth_bootstrap2(coup, crit, points, final_coup):  
    optimizer = minimize( lsqe, [np.average(crit), 0.0, 1.0, 1.0, 0.0], args=(np.array(coup),crit),
        jac=False, method='L-BFGS-B', options={'disp': False}, tol = 1e-6)
        
    x = optimizer.x 
    smooth_coup = np.linspace( np.min(final_coup), np.max(final_coup), points);
    smooth_crit = proposed_function(x, smooth_coup)
    
    return smooth_coup, smooth_crit

def color (number):
    return cm.ocean( number / 4.)
colours = [color(number) for number in range(0,4)]
fill_opacity = 0.7
def create_polygon( x1, x2, x3, x4, y1, y2, y3, y4, colour_index):
    global fill_opacity, colours
    x = np.array([])
    x = np.append(x, x1)
    x = np.append(x, x2)
    x = np.append(x, x3)
    x = np.append(x, x4)
    
    y = np.array([])
    y = np.append(y, y1)
    y = np.append(y, y2)
    y = np.append(y, y3)
    y = np.append(y, y4)
    
    vertices = np.zeros((x.shape[0], 2))
    vertices[:, 0] = x
    vertices[:, 1] = y 
    
    return plt.Polygon(vertices, zorder=0, facecolor=colours[colour_index], alpha=fill_opacity)
