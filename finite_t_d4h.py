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
colours_markers = [ 'r', 'k', 'b', 'm', 'y', 'g']

colours = [color(number) for number in range(0,4)]

shapes = ['v', '^', 'D', 'o', '8', 's', 'p']

fill_opacity = 0.7
marker_size = 100 #Just trial-error

x_tick = 0.1
y_tick = 0.1

min_y = 0.0
max_y = 3.00

min_x = 0.00
max_x = 2.0


x_tick_pad = 5
x_label_pad = 15
y_tick_pad = 5
y_label_pad = 25*2.7
x_label_text = "$\\beta J_3$"
y_label_text = "$\\beta J_1$"

extension = 'pdf'
#extension = 'png'
### 
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

#data

data_bl_one = np.array([])
data_bl_three = np.array([])

data_bu_one = np.array([2.7, 2.64, 2.58, 2.55, 2.55])
data_bu_three = np.array([0.00, 0.40, 1.00, 1.60, 2.00])

data_ul_one = np.array([2.10, 1.92, 1.55, 1.06, .68, 0.00])
data_ul_three = np.array([0.00, 0.40, 1.00, 1.40, 1.60, 1.80])

bu_three, bu_one = smooth_bootstrap(data_bu_three,data_bu_one, 100)
ul_three, ul_one = smooth_bootstrap(data_ul_three, data_ul_one, 100)

one = np.array([]) 
one = np.append(one, data_bl_one)
one = np.append(one, data_bu_one)
one = np.append(one, data_ul_one)

three = np.array([])
three = np.append(three, data_bl_three)
three = np.append(three, data_bu_three)
three = np.append(three, data_ul_three)

#smoothen data  
### markers 

color_count = -1

color_count += 1
ax.scatter(data_bl_three,  data_bl_one, zorder=1, color='b',  marker='D', s=marker_size)

color_count += 1
ax.scatter( data_bu_three, data_bu_one, zorder=1, color='m',  marker='o', s=marker_size)

color_count += 1
ax.scatter( data_ul_three, data_ul_one, zorder=1, color='k',  marker='^', s=marker_size)

# ax.scatter( .40, 2.08, zorder=2, color='r',  marker='*', s=1250)

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
    0, 
    [],
    ul_three,
    0,
    0,
    [],
    ul_one,
    0,
    2)
ax.add_patch(first_polygon)
ax.text( .50, 1.10, '$O(3)$', fontsize=75 )
second_polygon = create_polygon( 
   [], 
   bu_three,
   max_x,
   min_x,
   [],
   bu_one,
   max_y,
   max_y,
   0)
ax.add_patch(second_polygon) 
ax.text( 1.30, 1.80, '$D_{4h}$', fontsize=75 )
third_polygon = create_polygon( 
   ul_three,
   max_x,
   bu_three[::-1],
   [],
   ul_one,
   min_y,
   bu_one[::-1],
   [],
   1)
ax.add_patch(third_polygon) 
ax.text( .80, 2.70, '$D_{\\infty h}$', fontsize=75 )
###

###labels
ax.tick_params(axis='x', pad=x_tick_pad)
ax.tick_params(axis='y', pad=y_tick_pad)

ax.set_xlabel(x_label_text, fontsize=75, labelpad=x_label_pad)
ax.set_ylabel(y_label_text, fontsize=75, rotation=0, labelpad=y_label_pad)

 
plt.xticks(np.linspace(min_x, max_x, 5))
plt.xticks(np.array([0.00, 0.25, 0.50, 0.75, 1.00, 1.25, 1.50, 1.75, 2.00]))
plt.yticks(np.linspace(min_y, max_y, 5))
plt.yticks(np.array([0.00, 0.50, 1.00, 1.50, 2.00, 2.50, 3.00]))
 
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