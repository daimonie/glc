import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.ticker import AutoMinorLocator
from matplotlib import cm
from scipy.optimize import minimize
from smoother import *

#Feel free to change the colormap :-)
def color (number):
    return cm.ocean( number / 4.)
###parameters
colours_markers = [ 'r', 'k', 'b', 'c', 'm', 'y', 'g']
colours = [color(number) for number in range(0,4)]

shapes = ['v', '^', 'D', 'o', '8', 's', 'p']
labels = ['data biaxial-uniaxial','data biaxial-liquid', 'data uniaxial-liquid', 'uni-axial', 'bi-axial', 'isotropic liquid']

fill_opacity = .70
marker_size = 100 #Just trial-error

x_tick = 0.1
y_tick = 0.1

max_y = 3.0

x_tick_pad = 5
x_label_pad = 15

y_tick_pad = 5
y_label_pad = 50

x_label_text = "$J_1 \\left[J_3\\right]$"
y_label_text = "$T \\left[J_3\\right]$"

extension = 'pdf'
#extension = 'png'
###
print r"$\\beta_C$ data was inverted to find $T_C$."
#C_2 -> C_{\inf v}
biuni_coup = np.array([0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4])
biuni_crit = 1/np.array([1.21, 1.00, 0.88, 0.80, 0.740, 0.68, 0.64, 0.59, 0.57, 0.52])

#C_{\inf v} -> O(3)
unili_coup = np.array([0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4])
unili_crit = 1/np.array([0.62, 0.61, 0.60, 0.60, 0.59, 0.57, 0.56, 0.55, 0.54, 0.52])

#C_2 -> O(3)
biali_coup = np.array([1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5])
biali_crit = 1/np.array([0.52, 0.51, 0.50, 0.48, 0.47, 0.45, 0.44, 0.42, 0.41, 0.40, 0.39, 0.37])
#initialise figure
fig, ax = plt.subplots(1, 1, figsize=(25, 15), dpi=1080)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30) 
plt.rc('font', family='serif')

#smoothen data
rbiuni_coup, rbiuni_crit = biuni_coup, biuni_crit
runili_coup, runili_crit = unili_coup, unili_crit
rbiali_coup, rbiali_crit = biali_coup, biali_crit

biuni_coup, biuni_crit = smooth_bootstrap(biuni_coup, biuni_crit, 100)
unili_coup, unili_crit = smooth_bootstrap(unili_coup, unili_crit, 100)
biali_coup, biali_crit = smooth_bootstrap(biali_coup, biali_crit, 100)

### first filled shape, the biaxial phase 

first_dim0 = biuni_crit.shape[0]
first_dim1 = biali_crit.shape[0]

first_data = np.zeros((first_dim0 + first_dim1+1, 2))

first_data[0:first_dim0,0] =  biuni_coup
first_data[0:first_dim0,1] = biuni_crit

first_data[first_dim0:(first_dim0+first_dim1),0] = biali_coup
first_data[first_dim0:(first_dim0+first_dim1),1] = biali_crit 

first_data[first_dim0 + first_dim1, 0] = np.max( first_data[:,0])
first_data[first_dim0 + first_dim1, 1] = 0

first_polygon = plt.Polygon(first_data, zorder=0, facecolor=colours[0], alpha=fill_opacity)
ax.add_patch(first_polygon)

ax.text( 1.750, 1.5, '$C_{2}$', fontsize=40 )
ax.text( 1.750, 1.35, 'Biaxial', fontsize=40 )

### second filled shape, the uniaxial

second_dim0 = biuni_crit.shape[0]
second_dim1 = unili_crit.shape[0]

second_data = np.zeros((second_dim0 + second_dim1, 2))

second_data[0:second_dim0, 0] = biuni_coup
second_data[0:second_dim0, 1] = biuni_crit 
  
second_data[(second_dim0):(second_dim0+second_dim1), 0] = unili_coup[::-1]
second_data[(second_dim0):(second_dim0+second_dim1), 1] = unili_crit[::-1]
 
second_polygon = plt.Polygon(second_data, zorder=0, facecolor=colours[1], alpha=fill_opacity)
ax.add_patch(second_polygon)

ax.text( 0.65, 1.50, '$C_{\infty v}$', fontsize=40 )
ax.text( 0.55, 1.40, 'Uniaxial', fontsize=40 )

### third filled shape, the liquid phase 

third_dim0 = biali_crit.shape[0]
third_dim1 = unili_crit.shape[0]

third_data = np.zeros((third_dim0 + third_dim1+2, 2))

third_data[0:third_dim0, 0] = biali_coup[::-1]
third_data[0:third_dim0, 1] = biali_crit[::-1]

third_data[(third_dim0):(third_dim0 + third_dim1), 0] = unili_coup[::-1]
third_data[(third_dim0):(third_dim0 + third_dim1), 1] = unili_crit[::-1]

if max_y == 'auto':
    third_data[third_dim0 + third_dim1, 0] = np.min(third_data[:,0])
    third_data[third_dim0 + third_dim1, 1] = np.max(third_data[:,1])
    
    third_data[third_dim0 + third_dim1+1, 0] = np.max(third_data[:,0])
    third_data[third_dim0 + third_dim1+1, 1] = np.max(third_data[:,1])
else:
    third_data[third_dim0 + third_dim1, 0] = np.min(third_data[:,0])
    third_data[third_dim0 + third_dim1, 1] = max_y
    
    third_data[third_dim0 + third_dim1+1, 0] = np.max(third_data[:,0])
    third_data[third_dim0 + third_dim1+1, 1] = max_y
    
    

  
third_polygon = plt.Polygon(third_data, zorder=0, facecolor=colours[2], alpha=fill_opacity)

ax.add_patch(third_polygon)

ax.text( 1.25, 2.45, '$O(3)$', fontsize=40 )
ax.text( 1.20, 2.30, 'Liquid', fontsize=40 )

### markers 

ax.scatter( rbiuni_coup, rbiuni_crit, zorder=1, color=colours_markers[0],  marker=shapes[0], label=labels[0], s=marker_size)
ax.scatter( runili_coup, runili_crit, zorder=1,  color=colours_markers[1],  marker=shapes[1], label=labels[1], s=marker_size)
ax.scatter( rbiali_coup, rbiali_crit, zorder=1,  color=colours_markers[2],  marker=shapes[2], label=labels[2], s=marker_size)

###labels
ax.tick_params(axis='x', pad=x_tick_pad)
ax.tick_params(axis='y', pad=y_tick_pad)

ax.set_xlabel(x_label_text, fontsize=75, labelpad=x_label_pad)
ax.set_ylabel(y_label_text, fontsize=75, rotation=0, labelpad=y_label_pad)
###
min_x = np.min([ np.min(biuni_coup), np.min(unili_coup), np.min(biali_coup)])
max_x = np.max([ np.max(biuni_coup), np.max(unili_coup), np.max(biali_coup)])

min_y = np.min([ np.min(biuni_crit), np.min(unili_crit), np.min(biali_crit)])
if max_y == 'auto':
    max_y = int(np.max([ np.max(biuni_crit), np.max(unili_crit), np.max(biali_crit)]))
 
plt.xticks(np.arange(int(min_x/x_tick)*x_tick, max_x, .5))
plt.yticks(np.arange(int(min_y/y_tick)*y_tick, max_y, .5))
 
minorLocator1 = AutoMinorLocator(5)
minorLocator2 = AutoMinorLocator(5)
ax.xaxis.set_minor_locator(minorLocator1) 
ax.yaxis.set_minor_locator(minorLocator2) 

plt.tick_params(which='both', width=2)
plt.tick_params(which='major', length=20)
plt.tick_params(which='minor', length=10)

ax.set_xlim([min_x, max_x])
ax.set_ylim([min_y, max_y]) 

#plt.legend(bbox_to_anchor=(1.2, 1.1)) 
if extension == "png":
    plt.show()
else:
    plt.savefig('smooth.%s' % extension)