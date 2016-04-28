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
###parameters
colours_markers = [ 'r', 'k', 'b', 'c', 'm', 'y', 'g']

shapes = ['v', '^', 'D', 'o', '8', 's', 'p']

marker_size = 100 #Just trial-error

x_tick = 0.02
y_tick = 0.1

min_x = 0.00
max_x = 0.20

min_y = 0.00
max_y = 0.80

x_tick_pad = 5
x_label_pad = 15
y_tick_pad = 5
y_label_pad = 125
x_label_text = "$J_1 \\left[J_3\\right]$"
y_label_text = "$T\\, \\left[J_3\\right]$"

extension = 'pdf'
#extension = 'png'
###
data_s2_dinf_coup = np.array([0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, .09, 0.10])
data_s2_dinf_crit = np.array([float("Inf"), 13, 8.2, 5.5, 4.0, 3.3, 2.9, 2.5, 2.2, 2.0, 1.64])

data_s2_dinf_crit += -0.05*5
data_s2_dinf_crit[10] = 1.64
data_s2_dinf_crit = 1/data_s2_dinf_crit

s2_dinf_coup, s2_dinf_crit = smooth_bootstrap(data_s2_dinf_coup, data_s2_dinf_crit, 100)

data_dinfh_03_coup = np.array([0.00, 0.02, 0.04, 0.06, 0.08, 0.10])
data_dinfh_03_crit = 1/np.array([1.75, 1.72, 1.70, 1.67, 1.65, 1.64])
dinfh_03_coup, dinfh_03_crit = smooth_bootstrap(data_dinfh_03_coup, data_dinfh_03_crit, 100)

data_s2_03_coup = np.array([0.1, 0.12, 0.14, 0.16, 0.18, 0.20])
data_s2_03_crit = 1/np.array([1.64, 1.59, 1.55, 1.53, 1.50, 1.46])
s2_03_coup, s2_03_crit = smooth_bootstrap(data_s2_03_coup, data_s2_03_crit, 100)


###
coup = np.array([])
coup = np.append(coup, data_s2_dinf_coup)
coup = np.append(coup, data_dinfh_03_coup)
coup = np.append(coup, data_s2_03_coup)

crit = np.array([]) 
crit = np.append(crit, data_s2_dinf_crit) 
crit = np.append(crit, data_dinfh_03_crit) 
crit = np.append(crit, data_s2_03_crit) 
 
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
ax.scatter( data_s2_dinf_coup, data_s2_dinf_crit, zorder=1, color=colours_markers[color_count],  marker=shapes[color_count], s=marker_size)

color_count += 1
ax.scatter( data_dinfh_03_coup, data_dinfh_03_crit, zorder=1, color=colours_markers[color_count],  marker=shapes[color_count], s=marker_size)

color_count += 1
ax.scatter( data_s2_03_coup, data_s2_03_crit, zorder=1, color=colours_markers[color_count],  marker=shapes[color_count], s=marker_size)

###plot smooth
if False:
    plt.plot(s2_dinf_coup, s2_dinf_crit, "%s--" % colours_markers[0]) 
    plt.plot(dinfh_03_coup, dinfh_03_crit, "%s--" % colours_markers[1]) 
    plt.plot(s2_03_coup, s2_03_crit, "%s--" % colours_markers[1]) 
###
#polygons time 
first_polygon = create_polygon(
    s2_dinf_coup,
    dinfh_03_coup[::-1],
    min_x,
    min_x,
    s2_dinf_crit,
    dinfh_03_crit[::-1],
    min_y,
    min_y,
    0)
ax.add_patch(first_polygon)
ax.text( 0.012, .35 + 0.05, '$D_{\\infty h}$', fontsize=40 )
#ax.text( 0.01, .35 - 0.0, 'Uniaxial', fontsize=40 )
#polygons time 
second_polygon = create_polygon(
    dinfh_03_coup,
    s2_03_coup,
    max_x,
    min_x,
    dinfh_03_crit,
    s2_03_crit,
    max_y,
    max_y,
    2)
ax.add_patch(second_polygon) 
ax.text( .05, .6 + 0.05, '$O(3)$', fontsize=40 )
#ax.text( .05, .6 - 0.0, 'Liquid', fontsize=40 )
###
third_polygon = create_polygon(
    s2_dinf_coup,
    s2_03_coup,
    max_x,
    min_x,
    s2_dinf_crit,
    s2_03_crit,
    min_y,
    min_y,
    1)
ax.add_patch(third_polygon) 
ax.text( .105, .25 + 0.05, '$S_{2}\\simeq C_{i}$', fontsize=40 )
#ax.text( .1, .25 - 0.0, 'Biaxial', fontsize=40 )
### 
###labels
ax.tick_params(axis='x', pad=x_tick_pad)
ax.tick_params(axis='y', pad=y_tick_pad)

ax.set_xlabel(x_label_text, fontsize=75, labelpad=x_label_pad)
ax.set_ylabel(y_label_text, fontsize=75, rotation=0, labelpad=y_label_pad)

 
plt.xticks(np.linspace(min_x, max_x, 5))
plt.xticks(np.array([0.00, 0.05, 0.10, 0.15, 0.20]))
plt.yticks(np.linspace(min_y, max_y, 5))
plt.yticks(np.array([0.00, 0.25, 0.50, 0.75, 0.80]))
 
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