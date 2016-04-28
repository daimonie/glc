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

min_y = 0.600
max_y = 2.2

min_x = 0.50
max_x = 2.50


x_tick_pad = 5
x_label_pad = 15
y_tick_pad = 5
y_label_pad = 125
x_label_text = "$J_1 \\left[J_3\\right]$"
y_label_text = "$T\\, \\left[J_3\\right]$"

extension = 'pdf'
#extension = 'png'
###
 

data_c2v_cinf_coup = np.array([0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0])
data_c2v_cinf_crit = 1/np.array([1.66, 1.42, 1.25, 1.14, 1.00, .93, .85, .79, .74, .70, .67, .64, .61, .58, .56, .53])
c2v_cinf_coup, c2v_cinf_crit = smooth_bootstrap(data_c2v_cinf_coup, data_c2v_cinf_crit, 100)

data_cinf_03_coup = np.array([.5, .6, .7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0])
data_cinf_03_crit = 1/np.array([.62, .62, .62, .60, .60, .60, .60, .58, .58, .56, .56, .55, .55, .54, .53, .53])
cinf_03_coup, cinf_03_crit = smooth_bootstrap(data_cinf_03_coup, data_cinf_03_crit, 100)

data_c2v_03_coup = np.array([2.0, 2.1, 2.2, 2.3, 2.4, 2.5])
data_c2v_03_crit = 1/np.array([0.53, 0.52, .51, .5, .49, .48])
c2v_03_coup, c2v_03_crit = smooth_bootstrap(data_c2v_03_coup, data_c2v_03_crit,100)

comp_coup = np.append( data_cinf_03_coup, data_c2v_03_coup)
comp_crit = np.append( data_cinf_03_crit, data_c2v_03_crit)

for i in range(3):
    comp_coup = np.append( comp_coup, np.min(data_c2v_03_coup))
    comp_crit = np.append( comp_crit, np.min(data_c2v_03_crit))
    
c2v_03_coup, c2v_03_crit = smooth_bootstrap2(comp_coup, comp_crit,100, data_c2v_03_coup)



###
coup = np.array([])
coup = np.append(coup, data_c2v_cinf_coup)  
coup = np.append(coup, data_cinf_03_coup)  
coup = np.append(coup, data_c2v_03_coup)  

crit = np.array([]) 
crit = np.append(crit, data_c2v_cinf_crit)  
crit = np.append(crit, data_cinf_03_crit)  
crit = np.append(crit, data_c2v_03_crit)  
 
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
ax.scatter( data_c2v_cinf_coup, data_c2v_cinf_crit, zorder=1, color=colours_markers[color_count],  marker=shapes[color_count], s=marker_size)
  
color_count += 1
ax.scatter( data_cinf_03_coup, data_cinf_03_crit, zorder=1, color=colours_markers[color_count],  marker=shapes[color_count], s=marker_size)

color_count += 1
ax.scatter( data_c2v_03_coup, data_c2v_03_crit, zorder=1, color=colours_markers[color_count],  marker=shapes[color_count], s=marker_size)
  
###plot smooth
if False:
    plt.plot(c2v_cinf_coup, c2v_cinf_crit, "%s--" % colours_markers[0])
    plt.plot(cinf_03_coup, cinf_03_crit, "%s--" % colours_markers[0])
    plt.plot(c2v_03_coup, c2v_03_crit, "%s--" % colours_markers[0])
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
    c2v_cinf_coup,
    cinf_03_coup[::-1],
    min_x,
    min_x,
    c2v_cinf_crit,
    cinf_03_crit[::-1], 
    min_y,
    min_y,
    0)
ax.add_patch(first_polygon)
ax.text( 0.82, 1.35 + 0.05, '$C_{\\infty v}$', fontsize=40 )
#ax.text( 0.75, 1.35 - 0.05, 'Uniaxial', fontsize=40 )
###

second_polygon = create_polygon(
    c2v_cinf_coup,
    c2v_03_coup,
    max_x,
    min_x,
    c2v_cinf_crit,
    c2v_03_crit, 
    min_y,
    min_y,
    1)
ax.add_patch(second_polygon)
ax.text( 1.82, 1.15 + 0.05, '$C_{2 v}$', fontsize=40 )
#ax.text( 1.75, 1.15 - 0.05, 'Biaxial', fontsize=40 )

###

third_polygon = create_polygon(
    cinf_03_coup,
    c2v_03_coup,
    max_x,
    min_x, 
    cinf_03_crit,
    c2v_03_crit,
    max_y,
    max_y, 
    2)
ax.add_patch(third_polygon)
ax.text( 1.27, 1.95 + 0.05, '$O(3)$', fontsize=40 )
#ax.text( 1.25, 1.95 - 0.05, 'Liquid', fontsize=40 )
###labels
ax.tick_params(axis='x', pad=x_tick_pad)
ax.tick_params(axis='y', pad=y_tick_pad)

ax.set_xlabel(x_label_text, fontsize=75, labelpad=x_label_pad)
ax.set_ylabel(y_label_text, fontsize=75, rotation=0, labelpad=y_label_pad)

 
plt.xticks(np.linspace(min_x, max_x, 5))
plt.yticks(np.linspace(min_y, max_y, 5))


plt.yticks(np.array([0.00, 0.50, 1.00, 1.50, 2.00, 2.20]))
 
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