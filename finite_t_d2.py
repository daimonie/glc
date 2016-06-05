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
# biaxial uniaxial bu
# uniaxial liquid ul
# biaxial liquid bl
# biaxial biaxial-star bs
# biaxial-star liquid sl

data_bu_three = np.array([1.5, 1.75, 2.0])
data_bu_one = np.array([.86, .80, .74])
bu_three, bu_one = smooth_bootstrap(data_bu_three, data_bu_one, 100)

data_ul_three = np.array([1.5, 1.6, 1.75])
data_ul_one = np.array([.86, .62, 0.00])
ul_three, ul_one = smooth_bootstrap(data_ul_three, data_ul_one, 100)

data_bl_three = np.array([.60, .80, 1.00, 1.20, 1.50])
data_bl_one = np.array([1.28, 1.20, 1.08, .98, .86])
bl_three, bl_one = smooth_bootstrap(data_bl_three, data_bl_one, 100)

data_bs_three = np.array([0.20, .27, 0.30, 0.40, 0.45, 0.6])
data_bs_one = np.array([3.00, 2.50,2.00, 1.59, 1.50, 1.28])
bs_three, bs_one = smooth_bootstrap(data_bs_three, data_bs_one, 100)

data_sl_three = np.array([0.00, 0.30, .60])
data_sl_one = np.array([1.36, 1.30, 1.28])
sl_three, sl_one = smooth_bootstrap(data_sl_three, data_sl_one, 100)

one = np.array([]) 
one = np.append(one, data_bu_one) 
one = np.append(one, data_ul_one) 
one = np.append(one, data_bl_one) 
one = np.append(one, data_bs_one) 
one = np.append(one, data_sl_one) 

three = np.array([])
three = np.append(three, data_bu_three)
three = np.append(three, data_ul_three)
three = np.append(three, data_bl_three)
three = np.append(three, data_bs_three)
three = np.append(three, data_sl_three)

#smoothen data 
smooth_three = np.append(data_sl_three, data_bl_three)
smooth_one = np.append(data_sl_one, data_bl_one)
for i in range(5):
    smooth_three = np.append(smooth_three, .60)
    smooth_one = np.append(smooth_one, 1.28)
    
    smooth_three = np.append(smooth_three, 1.50)
    smooth_one = np.append(smooth_one, .86)
    
for i in range(5):
    smooth_three = np.append(smooth_three, 1.20)
    smooth_one = np.append(smooth_one, 0.98)
    
    
sl_three, sl_one = smooth_bootstrap2( smooth_three, smooth_one, 100, data_sl_three)
bl_three, bl_one = smooth_bootstrap2( smooth_three, smooth_one, 100, data_bl_three)


smooth_three = np.append(data_bs_three, bl_three)
smooth_one = np.append(data_bs_one, bl_one)
for i in range(500):
    smooth_three = np.append(smooth_three, .60)
    smooth_one = np.append(smooth_one, 1.28)
    
    smooth_three = np.append(smooth_three, 1.50)
    smooth_one = np.append(smooth_one, .86)
    
bs_three, bs_one = smooth_bootstrap2( smooth_three, smooth_one, 100, data_sl_three)

### markers 

color_count = -1

color_count += 1
ax.scatter(data_bu_three,  data_bu_one, zorder=1, color='m',  marker='o', s=marker_size)

color_count += 1
ax.scatter(data_ul_three,  data_ul_one, zorder=1, color='k',  marker='^', s=marker_size)

color_count += 1
ax.scatter(data_bl_three,  data_bl_one, zorder=1, color='b',  marker='D', s=marker_size)

color_count += 1
ax.scatter(data_bs_three,  data_bs_one, zorder=1, color='g',  marker='s', s=marker_size)

color_count += 1
ax.scatter(data_sl_three,  data_sl_one, zorder=1, color='r',  marker='v', s=marker_size)

# tricritical point
ax.scatter( .60, 1.28, zorder=2, color='b',  marker='*', s=1250)
ax.scatter( 1.50, .86, zorder=2, color='r',  marker='*', s=1250)

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
    sl_three,
    bl_three, 
    ul_three,
    0,
    sl_one,
    bl_one,
    ul_one,
    2)
ax.add_patch(first_polygon) 
ax.text( .65, .45, '$O(3)$', fontsize=75 ) 
###
second_polygon = create_polygon( 
    sl_three,
    bs_three[::-1],
    min_x,
    [],
    sl_one,
    bs_one[::-1],
    max_y,
    [],
    3)
ax.add_patch(second_polygon) 
ax.text( .10, 1.65, '$D_{2h}$', fontsize=75 ) 
###
third_polygon = create_polygon( 
    bs_three,
    bl_three,
    bu_three,
    [max_x, min_x],
    bs_one,
    bl_one,
    bu_one,
    [max_y, max_y],
    0)
ax.add_patch(third_polygon) 
ax.text( .90, 1.65, '$D_{2}$', fontsize=75 ) 
###
fourth_polygon = create_polygon( 
    bu_three,
    max_x,
    ul_three[::-1],
    [],
    bu_one,
    min_y,
    ul_one[::-1],
    [],
    1)
ax.add_patch(fourth_polygon) 
ax.text( 1.65, .55, '$D_{\\infty h}$', fontsize=75 ) 
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