import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.ticker import AutoMinorLocator
from matplotlib import cm
from matplotlib.ticker import FormatStrFormatter
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

min_x = 0.0
min_y = 0.0

max_x = 1.25 
max_y = 1.20

x_tick_pad = 5
x_label_pad = 15
y_tick_pad = 5
y_label_pad = 125
x_label_text = "$J_1 \\left[J_3\\right]$"
y_label_text = "$T\\, \\left[J_3\\right]$"

extension = 'pdf'
#extension = 'png'
###
print r"$\\beta_C$ data was inverted to find $T_C$."
#C_2 -> C_{\inf v}
biuni_coup = np.array([0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60])
biuni_crit = 1/np.array([float('Inf'), 13, 7.1, 4.8, 3.8, 2.8, 2.36, 2.1, 1.89, 1.74, 1.63, 1.54, 1.46])

#C_{\inf v} -> O(3)
unili_coup = np.array([0.00, 0.05, 0.10, 0.15, 0.25, 0.35, 0.40, 0.45, 0.50, 0.60])
unili_crit = 1/np.array([1.8, 1.72, 1.71, 1.70, 1.68, 1.63, 1.6, 1.55, 1.5, 1.46])

#C_2 -> O(3)
biali_coup = np.array([.60, .65, .75, .80, .85, .90, .95, 1.05, 1.10, 1.15, 1.20, 1.25])
biali_crit = 1/np.array([1.46, 1.39, 1.27, 1.22, 1.18, 1.13, 1.09, 1.02, .99, .96, .93, .91])
#initialise figure
fig, ax = plt.subplots(1, 1, figsize=(25, 15), dpi=1080)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30) 
plt.rc('font', family='serif')
fig.subplots_adjust(left=0.17)

#smoothen data
rbiuni_coup, rbiuni_crit = biuni_coup, biuni_crit
runili_coup, runili_crit = unili_coup, unili_crit
rbiali_coup, rbiali_crit = biali_coup, biali_crit

biuni_coup, biuni_crit = smooth_bootstrap(biuni_coup, biuni_crit, 100)
unili_coup, unili_crit = smooth_bootstrap(unili_coup, unili_crit, 100)
biali_coup, biali_crit = smooth_bootstrap(biali_coup, biali_crit, 100)


### first filled shape, the biaxial phase 
 
first_polygon = create_polygon(
    biuni_coup,
    biali_coup,
    max_x,
    max_x,
    biuni_crit,
    biali_crit, 
    min_y,
    min_y,
    1)

ax.add_patch(first_polygon)

first_average_coup = .7
first_average_crit = .5
ax.text( first_average_coup+.05, .5*first_average_crit+0.05, '$D_{2}$', fontsize=40 )
#ax.text( first_average_coup, .5*first_average_crit-0.05, 'Biaxial', fontsize=40 )

### second filled shape, the uniaxial

second_polygon = create_polygon(
    biuni_coup,
    unili_coup[::-1],
    min_x,
    min_x,
    biuni_crit,
    unili_crit[::-1], 
    min_y,
    min_y,
    0)


ax.add_patch(second_polygon)
 
ax.text( 0.07+.05, .4 + 0.05, '$D_{\infty h}$', fontsize=40 )
#ax.text( 0.07, .4 - 0.05, 'Uniaxial', fontsize=40 )

### third filled shape, the liquid phase 

third_dim0 = biali_crit.shape[0]
third_dim1 = unili_crit.shape[0]
 
third_polygon = create_polygon(
    unili_coup,
    biali_coup,
    max_x,
    min_x,
    unili_crit,
    biali_crit, 
    max_y,
    max_y,
    2)
ax.add_patch(third_polygon)
ax.text( .55, .9, '$O(3)$', fontsize=40 )
#ax.text( .5, .85, 'Liquid', fontsize=40 )

### markers 

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
 
plt.xticks(np.linspace(min_x, max_x, 5))
plt.xticks(np.array([0.00, 0.25, 0.50, 0.75, 1.00, 1.25]))
plt.yticks(np.linspace(min_y, max_y, 5))
plt.yticks(np.array([0.00, 0.25, 0.50, 0.75, 1.00, 1.20]))
 
minorLocator1 = AutoMinorLocator(5)
minorLocator2 = AutoMinorLocator(5)
ax.xaxis.set_minor_locator(minorLocator1) 
ax.yaxis.set_minor_locator(minorLocator2) 

ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

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