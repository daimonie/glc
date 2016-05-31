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

fill_opacity = 0.7
marker_size = 100 #Just trial-error

x_tick = 0.1
y_tick = 0.1

min_x = 0.00
max_x = 1.50

min_y = 0.0
max_y = 1.1

x_tick_pad = 5
x_label_pad = 15
y_tick_pad = 5
y_label_pad = 125
x_label_text = "$J_3 \\left[J_1\\right]$"
y_label_text = "$T\\, \\left[J_1\\right]$"

extension = 'pdf'
#extension = 'png'
###
print r"$\\beta_C$ data was inverted to find $T_C$. Also, I've cheated a little bit to make the smooth lines fit better."
 
data_d2d_d4h_coup = np.array([0.00, 0.04, 0.08, 0.12, 0.16, .20, .24, .28, .30, .32, .34])
data_d2d_d4h_crit = 1/np.array([float("Inf"),9.5, 6.0, 3.0, 2.5, 2.25, 2.13, 2.03, 2.00, 1.96, 1.92])

#taking some liberty with the margins
data_d2d_d4h_crit[2]  += 0.1/2.0
data_d2d_d4h_crit[3]  -= 0.1/2.0
data_d2d_d4h_crit[4]  -= 0.1/2.0
data_d2d_d4h_crit[5]  -= 0.1/2.0
data_d2d_d4h_crit[6]  -= 0.1/2.0

d2d_d4h_coup, d2d_d4h_crit = smooth_bootstrap( data_d2d_d4h_coup, data_d2d_d4h_crit, 100)

data_d4h_03_coup = np.array([0.00, 0.04, 0.08, 0.12, 0.16, 0.20, 0.24, 0.28, 0.32, 0.34])
data_d4h_03_crit = 1/np.array([2.10, 2.08, 2.06, 2.04, 2.02, 2.00, 1.98, 1.96, 1.94, 1.92])
d4h_03_coup, d4h_03_crit = smooth_bootstrap( data_d4h_03_coup, data_d4h_03_crit, 100)

data_d2d_03_coup =  np.array([0.34, 0.36, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.0, 1.1])
data_d2d_03_crit = 1/np.array([1.92, 1.89, 1.83, 1.72, 1.61, 1.52, 1.45, 1.39, 1.33, 1.27])
d2d_03_coup, d2d_03_crit =  smooth_bootstrap( data_d2d_03_coup, data_d2d_03_crit, 100)

data_d2d_dinfh_coup =  np.array([1.1, 1.2, 1.3, 1.4, 1.5])
data_d2d_dinfh_crit = 1/np.array([1.27, 1.24, 1.21, 1.18, 1.15])
d2d_dinfh_coup, d2d_dinfh_crit = smooth_bootstrap( data_d2d_dinfh_coup, data_d2d_dinfh_crit, 100)

data_dinfh_03_coup =  np.array([1.1, 1.2, 1.3, 1.4, 1.5])
data_dinfh_03_crit = 1/np.array([1.27, 1.17, 1.09, 1.02, 0.95])
dinfh_03_coup, dinfh_03_crit = smooth_bootstrap( data_dinfh_03_coup, data_dinfh_03_crit, 100)


coup = np.array([]) 
coup = np.append(coup, data_d2d_d4h_coup)
coup = np.append(coup, data_d4h_03_coup)
coup = np.append(coup, data_d2d_03_coup)
coup = np.append(coup, data_d2d_dinfh_coup)
coup = np.append(coup, data_dinfh_03_coup)

crit = np.array([]) 
crit = np.append(crit, data_d2d_d4h_crit)
crit = np.append(crit, data_d4h_03_crit)
crit = np.append(crit, data_d2d_03_crit)
crit = np.append(crit, data_d2d_dinfh_crit)
crit = np.append(crit, data_dinfh_03_crit)
###
if max_x == 'auto':
    min_x = np.min(coup)
    max_x = np.max(coup)

if max_y == 'auto':
    min_y = np.min(crit)
    max_y = int(np.max(crit))
    
#initialise figure
fig, ax = plt.subplots(1, 1, figsize=(25, 15), dpi=1080)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30) 
plt.rc('font', family='serif')
fig.subplots_adjust(left=0.17)

#smoothen data 
#rbiali_coup, rbiali_crit = biali_coup, biali_crit 
#biali_coup, biali_crit = smooth_bootstrap(biali_coup, biali_crit, 100)
 
### markers 

color_count = -1

color_count += 1
ax.scatter( data_d2d_d4h_coup, data_d2d_d4h_crit, zorder=1, color=colours_markers[color_count],  marker=shapes[color_count], s=marker_size)
  
color_count += 1
ax.scatter( data_d4h_03_coup, data_d4h_03_crit, zorder=1, color=colours_markers[color_count],  marker=shapes[color_count], s=marker_size)
  
color_count += 1
ax.scatter( data_d2d_03_coup, data_d2d_03_crit, zorder=1, color=colours_markers[color_count],  marker=shapes[color_count], s=marker_size)
  
color_count += 1
ax.scatter( data_d2d_dinfh_coup, data_d2d_dinfh_crit, zorder=1, color=colours_markers[color_count],  marker=shapes[color_count], s=marker_size)
  
color_count += 1
ax.scatter( data_dinfh_03_coup, data_dinfh_03_crit, zorder=1, color=colours_markers[color_count],  marker=shapes[color_count], s=marker_size)
  
###plot smooth
if False:
    plt.plot(d2d_d4h_coup, d2d_d4h_crit, "%s--" % colours_markers[0])
    plt.plot(d4h_03_coup, d4h_03_crit, "%s--" % colours_markers[1])
    plt.plot(d2d_03_coup, d2d_03_crit, "%s--" % colours_markers[2])
    plt.plot(d2d_dinfh_coup, d2d_dinfh_crit, "%s--" % colours_markers[3])
    plt.plot(dinfh_03_coup, dinfh_03_crit, "%s--" % colours_markers[4])
###
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

# polygons!
first_polygon = create_polygon(
    d2d_d4h_coup, 
    d4h_03_coup[::-1],
    min_x,
    min_x,
    d2d_d4h_crit,
    d4h_03_crit[::-1],
    d4h_03_crit.max(),
    min_y,
    3)
ax.add_patch(first_polygon)
#ax.text( 0.05, .35, '$D_{4h}$', fontsize=40 )
ax.text( 0.01, .35, '$D_{4h}$', fontsize=75 )
#ax.text( 0., .5 - 0.05, 'Biaxial', fontsize=40 )
###
second_polygon = create_polygon(
    d2d_d4h_coup, 
    d2d_03_coup,
    d2d_dinfh_coup,
    max_x,
    d2d_d4h_crit, 
    d2d_03_crit,
    d2d_dinfh_crit,
    min_y,
    1)
ax.add_patch(second_polygon)
#ax.text( 0.85, .40, '$D_{2d}$', fontsize=40 )
ax.text( 0.85, .40, '$D_{2d}$', fontsize=75 )
### 
###
third_polygon = create_polygon(
    d2d_dinfh_coup,
    dinfh_03_coup[::-1],
    [],
    [],
    d2d_dinfh_crit,
    dinfh_03_crit[::-1],
    [],
    [],
    0)
ax.add_patch(third_polygon)
#ax.text( 1.35, .9, '$D_{\\infty h}$', fontsize=40 )
ax.text( 1.30, .9, '$D_{\\infty h}$', fontsize=75 )
###
fourth_polygon = create_polygon(
    d4h_03_coup,
    d2d_03_coup,
    dinfh_03_coup,
    np.array([max_x, min_x]),
    d4h_03_crit,
    d2d_03_crit,
    dinfh_03_crit,
    np.array([max_y,max_y]),
    2)
ax.add_patch(fourth_polygon)
#ax.text( 0.50, 0.90, '$O(3)$', fontsize=40 )
ax.text( 0.50, 0.90, '$O(3)$', fontsize=75 )
### 


###labels
ax.tick_params(axis='x', pad=x_tick_pad)
ax.tick_params(axis='y', pad=y_tick_pad)

ax.set_xlabel(x_label_text, fontsize=75, labelpad=x_label_pad)
ax.set_ylabel(y_label_text, fontsize=75, rotation=0, labelpad=y_label_pad)

 
plt.xticks(np.linspace(min_x, max_x, 5))
plt.xticks(np.array([0.00, 0.25, 0.50, 0.75, 1.00, 1.25, 1.50]))
plt.yticks(np.linspace(min_y, max_y, 5))
plt.yticks(np.array([0.00, 0.25, 0.50, 0.75, 1.00, 1.1]))
 
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