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

min_x = 0.000
max_x = 1.20
min_y = 0.000
max_y = 1.2
 

x_tick_pad = 5
x_label_pad = 15
y_tick_pad = 5
y_label_pad = 125
x_label_text = "$J_1 \\left[J_3\\right]$"
y_label_text = "$T\\, \\left[J_3\\right]$"

extension = 'pdf'
#extension = 'png'
###
data_d2h_dinf_coup = np.array([0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.35, 0.45, 0.55, 0.65])
data_d2h_dinf_crit = 1/np.array([float("Inf"), 13.2, 6.8, 4.8, 4.35, 3.0, 2.3, 1.85, 1.65, 1.44])
d2h_dinf_coup, d2h_dinf_crit = smooth_bootstrap(data_d2h_dinf_coup, data_d2h_dinf_crit, 100)

data_dinfh_03_coup = np.array([0.00, 0.05, 0.10, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65])
data_dinfh_03_crit = 1/np.array([1.8, 1.73, 1.72, 1.7, 1.68, 1.63, 1.56, 1.51, 1.44])
dinfh_03_coup, dinfh_03_crit = smooth_bootstrap(data_dinfh_03_coup, data_dinfh_03_crit, 100)

data_d2h_03_coup = np.array([0.65, 0.70, 0.75, 0.85, 0.90, 0.95, 1.05, 1.10, 1.15, 1.20, 1.25, ])
data_d2h_03_crit = 1/np.array([1.44, 1.40, 1.35, 1.25, 1.21, 1.17, 1.09, 1.05, 1.02, 0.98, 0.95])
d2h_03_coup, d2h_03_crit = smooth_bootstrap(data_d2h_03_coup, data_d2h_03_crit, 100)

###
coup = np.array([])
coup = np.append(coup, data_d2h_dinf_coup)
coup = np.append(coup, data_dinfh_03_coup)
coup = np.append(coup, data_d2h_03_coup)

crit = np.array([]) 
crit = np.append(crit, data_d2h_dinf_crit) 
crit = np.append(crit, data_dinfh_03_crit) 
crit = np.append(crit, data_d2h_03_crit) 
 
###
if max_x == 'auto':
    min_x = np.min(coup)
    max_x = np.max(coup)  
if max_y == 'auto':
    min_y = np.min(crit)
    max_y = np.max(crit)
print "window [%.3f, %.3f]x[%.3f, %.3f]" % (min_x, max_x, min_y, max_y)
#initialise figure
fig, ax = plt.subplots(1, 1, figsize=(25, 15), dpi=1080)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30) 
plt.rc('font', family='serif')
fig.subplots_adjust(left=0.17)

#smoothen data 
 
### markers 

color_count = -1

color_count += 1
ax.scatter( data_d2h_dinf_coup, data_d2h_dinf_crit, zorder=1, color=colours_markers[color_count],  marker=shapes[color_count], s=marker_size)

color_count += 1
ax.scatter( data_dinfh_03_coup, data_dinfh_03_crit, zorder=1, color=colours_markers[color_count],  marker=shapes[color_count], s=marker_size)

color_count += 1
ax.scatter( data_d2h_03_coup, data_d2h_03_crit, zorder=1, color=colours_markers[color_count],  marker=shapes[color_count], s=marker_size)

###plot smooth
if False:
    plt.plot(d2h_dinf_coup, d2h_dinf_crit, "%s--" % colours_markers[0]) 
    plt.plot(dinfh_03_coup, dinfh_03_crit, "%s--" % colours_markers[1]) 
    plt.plot(d2h_03_coup, d2h_03_crit, "%s--" % colours_markers[1]) 
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
#polygons time 
first_polygon = create_polygon(
    d2h_dinf_coup,
    dinfh_03_coup[::-1],
    min_x,
    min_x,
    d2h_dinf_crit,
    dinfh_03_crit[::-1],
    min_y,
    min_y,
    0)
ax.add_patch(first_polygon)
ax.text( 0.08, .35 + 0.05, '$D_{\\infty h}$', fontsize=40 )
#ax.text( 0.05, .35 - 0.0, 'Uniaxial', fontsize=40 )
#polygons time 
second_polygon = create_polygon(
    dinfh_03_coup,
    d2h_03_coup,
    max_x,
    min_x,
    dinfh_03_crit,
    d2h_03_crit,
    max_y,
    max_y,
    2)
ax.add_patch(second_polygon) 
ax.text( .45, .85 + 0.05, '$O(3)$', fontsize=40 )
#ax.text( .4, .85 - 0.0, 'Liquid', fontsize=40 )
###
third_polygon = create_polygon(
    d2h_dinf_coup,
    d2h_03_coup,
    max_x,
    min_x,
    d2h_dinf_crit,
    d2h_03_crit,
    min_y,
    min_y,
    1)
ax.add_patch(third_polygon) 
ax.text( .75, .35 + 0.05, '$D_{2h}$', fontsize=40 )
#ax.text( .7, .35 - 0.0, 'Biaxial', fontsize=40 )
### 
###labels
ax.tick_params(axis='x', pad=x_tick_pad)
ax.tick_params(axis='y', pad=y_tick_pad)

ax.set_xlabel(x_label_text, fontsize=75, labelpad=x_label_pad)
ax.set_ylabel(y_label_text, fontsize=75, rotation=0, labelpad=y_label_pad)

 
plt.xticks(np.linspace(min_x, max_x, 5))
plt.xticks(np.array([0.00, 0.25, 0.50, 0.75, 1.00, 1.20]))
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