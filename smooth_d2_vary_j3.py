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

fill_opacity = .70
marker_size = 100 #Just trial-error

x_tick = 0.1
y_tick = 0.1

max_y = 2.0

x_tick_pad = 5
x_label_pad = 15

y_tick_pad = 5
y_label_pad = 50

x_label_text = "$J_1 \\left[J_3\\right]$"
y_label_text = "$T \\left[J_3\\right]$"

extension = 'pdf'
#extension = 'png'
###
print r"$\\beta_C$ data was inverted to find $T_C$. Also, I've cheated a little bit to make the smooth lines fit better."

data_dtwodtwoh_coup = np.array([0.0, 0.2, 0.3, 0.4, 0.5, .6])
data_dtwodtwoh_crit = 1/np.array([float("Inf"), 1.72, 1.49, 1.38, 1.3, 1.23])

dtwodtwoh_coup, dtwodtwoh_crit = smooth_bootstrap(data_dtwodtwoh_coup, data_dtwodtwoh_crit, 100)


data_dtwohothree_coup = np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, .6])
data_dtwohothree_crit = 1/np.array([1.36, 1.36, 1.36, 1.34, 1.32, 1.3, 1.23])

dtwohothree_coup, dtwohothree_crit = smooth_bootstrap(data_dtwohothree_coup, data_dtwohothree_crit, 100)

data_dtwoothree_coup = np.array([0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8])
data_dtwoothree_crit = 1/np.array([1.23, 1.18, 1.14, 1.09, 1.06, 1.02, .99, .96, .94, .91, .89, .87, .85])

dtwoothree_coup, dtwoothree_crit = smooth_bootstrap(data_dtwoothree_coup, data_dtwoothree_crit, 100)

data_d2dinfh_coup = np.array([1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0])
data_d2dinfh_crit = 1/np.array([0.85, 0.83, 0.82, .80, 0.79, .78, .77, .76, .75, .74, .73, .73, .72])
d2dinfh_coup,d2dinfh_crit = smooth_bootstrap(data_d2dinfh_coup, data_d2dinfh_crit, 100)

data_dinfhothree_coup = np.array([1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0])
data_dinfhothree_crit = 1/np.array([0.84, 0.80, 0.76, 0.74, 0.71, 0.69, 0.66, 0.64, 0.62, 0.60, 0.58, 0.56, 0.54])
dinfhothree_coup, dinfhothree_crit = smooth_bootstrap(data_dinfhothree_coup, data_dinfhothree_crit, 100)

coup = np.array([])
coup = np.append(coup, data_dtwodtwoh_coup)
coup = np.append(coup, data_dtwohothree_coup)
coup = np.append(coup, data_dtwoothree_coup)
coup = np.append(coup, data_d2dinfh_coup)
coup = np.append(coup, data_dinfhothree_coup)

crit = np.array([])
crit = np.append(coup, data_dtwodtwoh_crit)
crit = np.append(coup, data_dtwohothree_crit)
crit = np.append(coup, data_dtwoothree_crit)
crit = np.append(coup, data_d2dinfh_crit)
crit = np.append(coup, data_dinfhothree_crit) 

#initialise figure
fig, ax = plt.subplots(1, 1, figsize=(25, 15), dpi=1080)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30) 
plt.rc('font', family='serif')

#smoothen data 
#rbiali_coup, rbiali_crit = biali_coup, biali_crit 
#biali_coup, biali_crit = smooth_bootstrap(biali_coup, biali_crit, 100)
 
### markers 

color_count = -1

color_count += 1
ax.scatter( data_dtwodtwoh_coup, data_dtwodtwoh_crit, zorder=1, color=colours_markers[color_count],  marker=shapes[color_count], s=marker_size)
 
color_count += 1
ax.scatter( data_dtwohothree_coup, data_dtwohothree_crit, zorder=1, color=colours_markers[color_count],  marker=shapes[color_count],  s=marker_size)
 
color_count += 1
ax.scatter( data_dtwoothree_coup, data_dtwoothree_crit, zorder=1, color=colours_markers[color_count],  marker=shapes[color_count],  s=marker_size)
 
color_count += 1
ax.scatter( data_d2dinfh_coup, data_d2dinfh_crit, zorder=1, color=colours_markers[color_count],  marker=shapes[color_count],  s=marker_size)
 
color_count += 1
ax.scatter( data_dinfhothree_coup, data_dinfhothree_crit, zorder=1, color=colours_markers[color_count],  marker=shapes[color_count],  s=marker_size)

###plot smooth
if True:
    plt.plot(dtwodtwoh_coup, dtwodtwoh_crit, "%s--" % colours_markers[0])
    plt.plot(dtwohothree_coup, dtwohothree_crit, "%s--" % colours_markers[1])
    plt.plot(dtwoothree_coup, dtwoothree_crit, "%s--" % colours_markers[2])
    plt.plot(d2dinfh_coup, d2dinfh_crit, "%s--" % colours_markers[3])
    plt.plot(dinfhothree_coup, dinfhothree_crit, "%s--" % colours_markers[4])
    
###
def create_polygon( x1, x2, x3, x4, y1, y2, y3, y4, colour_index):
    global fill_opacity
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
    dtwodtwoh_coup,
    dtwohothree_coup[::-1],
    0,
    0,####
    dtwodtwoh_crit,
    dtwohothree_crit[::-1], 
    np.max(dtwodtwoh_crit),
    0,###
    0)
ax.add_patch(first_polygon)
second_polygon = create_polygon(
    dtwodtwoh_coup,
    dtwoothree_coup,
    d2dinfh_coup,
    100,
    dtwodtwoh_crit,
    dtwoothree_crit,
    d2dinfh_crit,
    -100,
    1)
ax.add_patch(second_polygon)

third_polygon = create_polygon( 
    d2dinfh_coup[::-1], 
    dinfhothree_coup,
    100,
    100,
    d2dinfh_crit[::-1], 
    dinfhothree_crit,
    np.max(dinfhothree_crit),
    np.max(d2dinfh_crit),
    2)
ax.add_patch(third_polygon)

fourth_polygon = create_polygon( 
    dtwohothree_coup,
    dtwoothree_coup,
    dinfhothree_coup,
    -100,
    dtwohothree_crit,
    dtwoothree_crit,
    dinfhothree_crit,
    1e9,
    3)
ax.add_patch(fourth_polygon)

###labels
ax.tick_params(axis='x', pad=x_tick_pad)
ax.tick_params(axis='y', pad=y_tick_pad)

ax.set_xlabel(x_label_text, fontsize=75, labelpad=x_label_pad)
ax.set_ylabel(y_label_text, fontsize=75, rotation=0, labelpad=y_label_pad)
###
min_x = np.min(coup)
max_x = np.max(coup)

min_y = np.min(crit)
if max_y == 'auto':
    max_y = int(np.max(crit))
 
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