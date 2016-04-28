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
y_tick = 0.2

min_x = 0.00
max_x = 1.00

min_y = 0.00
max_y = 1.8


x_tick_pad = 5
x_label_pad = 15
y_tick_pad = 5
y_label_pad = 125
x_label_text = "$J_3 \\left[J_1\\right]$"
y_label_text = "$T\\, \\left[J_1\\right]$"

extension = 'pdf'
#extension = 'png'
###
 
data_c2_c2h_coup = np.array([0.0, 0.2, 0.3, 0.4])
data_c2_c2h_crit = 1/np.array([float('Inf'), 1.32, 1.05, .93])
c2_c2h_coup, c2_c2h_crit = smooth_bootstrap(data_c2_c2h_coup, data_c2_c2h_crit, 100)

data_c2h_03_coup = np.array([0.0, 0.1, 0.2, 0.3, 0.4])
data_c2h_03_crit = 1/np.array([0.96, 0.96, 0.95, 0.94, 0.93])
c2h_03_coup, c2h_03_crit = smooth_bootstrap(data_c2h_03_coup, data_c2h_03_crit, 100)

data_c2_03_coup = np.array([0.4, 0.5, 0.6, 0.7])
data_c2_03_crit = 1/np.array([0.93, 0.86, 0.80, 0.74])
c2_03_coup, c2_03_crit = smooth_bootstrap(data_c2_03_coup, data_c2_03_crit, 100)

data_c2_cinfv_coup = np.array([0.7, 0.8, 0.9, 1.0])
data_c2_cinfv_crit = 1/np.array([0.74, 0.72, 0.71, 0.68])
c2_cinfv_coup, c2_cinfv_crit = smooth_bootstrap(data_c2_cinfv_coup, data_c2_cinfv_crit, 100)

data_cinfv_03_coup = np.array([0.7, 0.8, 0.9, 1.0])
data_cinfv_03_crit = 1/np.array([0.74, 0.67, 0.62, 0.57])
cinfv_03_coup, cinfv_03_crit = smooth_bootstrap(data_cinfv_03_coup, data_cinfv_03_crit,100)

###
coup = np.array([])
coup = np.append(coup, data_c2_c2h_coup)
coup = np.append(coup, data_c2h_03_coup)
coup = np.append(coup, data_c2_03_coup)
coup = np.append(coup, data_c2_cinfv_coup)
coup = np.append(coup, data_cinfv_03_coup)

crit = np.array([]) 
crit = np.append(crit, data_c2_c2h_crit)  
crit = np.append(crit, data_c2h_03_crit)  
crit = np.append(crit, data_c2_03_crit)  
crit = np.append(crit, data_c2_cinfv_crit)  
crit = np.append(crit, data_cinfv_03_crit)  
 
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
ax.scatter( data_c2_c2h_coup, data_c2_c2h_crit, zorder=1, color=colours_markers[color_count],  marker=shapes[color_count], s=marker_size)
 
color_count += 1
ax.scatter( data_c2h_03_coup, data_c2h_03_crit, zorder=1, color=colours_markers[color_count],  marker=shapes[color_count], s=marker_size)
 
color_count += 1
ax.scatter( data_c2_03_coup, data_c2_03_crit, zorder=1, color=colours_markers[color_count],  marker=shapes[color_count], s=marker_size)
 
color_count += 1
ax.scatter( data_c2_cinfv_coup, data_c2_cinfv_crit, zorder=1, color=colours_markers[color_count],  marker=shapes[color_count], s=marker_size)
 
color_count += 1
ax.scatter( data_cinfv_03_coup, data_cinfv_03_crit, zorder=1, color=colours_markers[color_count],  marker=shapes[color_count], s=marker_size)
 
###plot smooth
if False:
    plt.plot(c2_c2h_coup, c2_c2h_crit, "%s--" % colours_markers[0]) 
    plt.plot(c2h_03_coup, c2h_03_crit, "%s--" % colours_markers[1])  
    plt.plot(c2_03_coup, c2_03_crit, "%s--" % colours_markers[2])  
    plt.plot(c2_cinfv_coup, c2_cinfv_crit, "%s--" % colours_markers[3])  
    plt.plot(cinfv_03_coup, cinfv_03_crit, "%s--" % colours_markers[3])  
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
    c2_c2h_coup,
    c2h_03_coup[::-1],
    min_x,
    min_x,
    c2_c2h_crit,
    c2h_03_crit[::-1], 
    min_y,
    min_y,
    3)
ax.add_patch(first_polygon)
ax.text( 0.075, .75 + 0.05, '$C_{2 h}$', fontsize=40 )
#ax.text( 0.05, .75-.05, 'Biaxial', fontsize=40 )
###
second_polygon = create_polygon(
    c2_c2h_coup,
    c2_03_coup,
    c2_cinfv_coup,
    max_x,
    c2_c2h_crit,
    c2_03_crit, 
    c2_cinfv_crit,
    min_y,
    1)
ax.add_patch(second_polygon)
ax.text( 0.575, .75 + 0.05, '$C_{2}$', fontsize=40 )
#ax.text( 0.55, .75-.05, 'Biaxial', fontsize=40 )
###
third_polygon = create_polygon(
    c2h_03_coup,
    c2_03_coup,
    cinfv_03_coup,
    np.array([max_x, min_x]),
    c2h_03_crit,
    c2_03_crit, 
    cinfv_03_crit,
    np.array([max_y, max_y]),
    2)
ax.add_patch(third_polygon)
ax.text( 0.375, 1.4 + 0.05, '$O(3)$', fontsize=40 )
#ax.text( 0.35, 1.4-.05, 'Liquid', fontsize=40 )
###
fourth_polygon = create_polygon(
    c2_cinfv_coup[::-1],
    cinfv_03_coup,
    [],
    [],
    c2_cinfv_crit[::-1],
    cinfv_03_crit, 
    [],
    [],
    0)
ax.add_patch(fourth_polygon)
ax.text( 0.90, 1.51 -0.02+ 0.05, '$C_{\\infty v}$', fontsize=40 )
#ax.text( 0.85, 1.51-.05, 'Uniaxial', fontsize=40 )
###labels
ax.tick_params(axis='x', pad=x_tick_pad)
ax.tick_params(axis='y', pad=y_tick_pad)

ax.set_xlabel(x_label_text, fontsize=75, labelpad=x_label_pad)
ax.set_ylabel(y_label_text, fontsize=75, rotation=0, labelpad=y_label_pad)

 
plt.xticks(np.linspace(min_x, max_x, 5))
plt.yticks(np.linspace(min_y, max_y, 5))
plt.yticks(np.array([0.00, 0.50, 1.00, 1.50, 1.80]))
 
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