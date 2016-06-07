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

max_x = 3.00
max_y = 2.50

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
biuni_coup = np.array([0.00, 0.10, 0.20, 0.30, 0.40, 0.50, 0.55, 0.60])
biuni_crit = 1/np.array([float('Inf'), 7.1, 3.8, 2.36, 1.89,1.63, 1.54, 1.46])

#C_{\inf v} -> O(3)
unili_coup = np.array([0.00,  0.10, 0.25, 0.40,  0.50, 0.60])
unili_crit = 1/np.array([1.8, 1.71, 1.68,  1.6, 1.5, 1.46])

#C_2 -> O(3)
biali_coup = np.array([.60, .65, .80,1.20, 1.60, 2.00, 2.20, 2.40])
biali_crit = 1/np.array([1.46, 1.39, 1.22, .93, .76, .64, .60, .56 ])

#D2 -> D2h
data_bs_coup = np.array([2.40, 2.60, 2.80, 3.00])
data_bs_crit = 1.0/np.array([.56, .53, .51, .48])

data_sl_coup = np.array([2.40, 2.60, 2.80, 3.00])
data_sl_crit = 1.0/np.array([.56, .50, .46, .43])

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


bs_coup, bs_crit = smooth_bootstrap2( np.append(biali_coup, data_bs_coup), np.append(biali_crit, data_bs_crit), 100, data_bs_coup)
sl_coup, sl_crit = smooth_bootstrap2( np.append(biali_coup, data_sl_coup), np.append(biali_crit, data_sl_crit), 100, data_sl_coup)

### first filled shape, the biaxial phase 
 
first_polygon = create_polygon(
    biuni_coup,
    biali_coup,
    bs_coup,
    max_x,
    
    biuni_crit,
    biali_crit, 
    bs_crit,
    min_y,
    0)

ax.add_patch(first_polygon)

first_average_coup = .7
first_average_crit = .5
ax.text( 1.75, .75, '$D_{2}$', fontsize=75 )
#ax.text( first_average_coup, .5*first_average_crit-0.05, 'Biaxial', fontsize=75 )

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
    1)


ax.add_patch(second_polygon)
 
ax.text( 0.05, .35  , '$D_{\infty h}$', fontsize=75 )
#ax.text( 0.07, .4 - 0.05, 'Uniaxial', fontsize=75 )

### third filled shape, the liquid phase 

third_dim0 = biali_crit.shape[0]
third_dim1 = unili_crit.shape[0]
 
third_polygon = create_polygon(
    unili_coup,
    biali_coup,
    sl_coup,
    [max_x, min_x],
    
    unili_crit,
    biali_crit, 
    sl_crit,
    [max_y, max_y],
    2)
ax.add_patch(third_polygon)
ax.text( .95, 1.59, '$O(3)$', fontsize=75 )
#ax.text( .5, .85, 'Liquid', fontsize=75 )

fourth_polygon = create_polygon(
    sl_coup,
    bs_coup[::-1],
    [],
    [],
    
    sl_crit,
    bs_crit[::-1],
    [],
    [],
    3)
ax.add_patch(fourth_polygon)
ax.text( 2.70, 2.1, '$D_{2 h}$', fontsize=75 )
### markers 

### markers 

ax.scatter( rbiuni_coup, rbiuni_crit, zorder=1, color='m',  marker='o', label=labels[0], s=marker_size)
ax.scatter( runili_coup, runili_crit, zorder=1,  color='k',  marker='^', label=labels[1], s=marker_size)
ax.scatter( rbiali_coup, rbiali_crit, zorder=1,  color='b',  marker='D', label=labels[2], s=marker_size)
ax.scatter( data_bs_coup, data_bs_crit, zorder=1,  color='g',  marker='s', label=labels[2], s=marker_size)
ax.scatter( data_sl_coup, data_sl_crit, zorder=1,  color='r',  marker='v', label=labels[2], s=marker_size)

ax.scatter( 2.40, 1.0/0.56, zorder=2, color='b',  marker='*', s=1250)
ax.scatter( .60, 1.0/1.46, zorder=2, color='r',  marker='*', s=1250)
###labels
ax.tick_params(axis='x', pad=x_tick_pad)
ax.tick_params(axis='y', pad=y_tick_pad)

ax.set_xlabel(x_label_text, fontsize=75, labelpad=x_label_pad)
ax.set_ylabel(y_label_text, fontsize=75, rotation=0, labelpad=y_label_pad)
###
plt.xticks(np.array(range(7))*.5)
plt.yticks(np.array(range(13))*.5)
 
minorLocator1 = AutoMinorLocator(5)
minorLocator2 = AutoMinorLocator(5)
ax.xaxis.set_minor_locator(minorLocator1) 
ax.yaxis.set_minor_locator(minorLocator2) 

ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

plt.tick_params(which='both', width=2)
plt.tick_params(which='major', length=20)
plt.tick_params(which='minor', length=10)

ax.set_xlim([0.00, max_x])
ax.set_ylim([0.00, max_y]) 

#plt.legend(bbox_to_anchor=(1.2, 1.1)) 
if extension == "png":
    plt.show()
else:
    plt.savefig('smooth.%s' % extension)