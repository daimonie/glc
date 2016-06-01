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

min_y = 0.0
max_y = 1.50

min_x = 0.00
max_x = 2.0


x_tick_pad = 5
x_label_pad = 15
y_tick_pad = 5
y_label_pad = 125
x_label_text = "$\\beta J_3$"
y_label_text = "$\\beta J_1$"

extension = 'pdf'
# extension = 'png'
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

data_bl_one = np.array([1.34, 1.32, 1.26, 1.18, 1.04])
data_bl_three = np.array([0.0, 0.4, 0.8, 1.0, 1.3])

data_bu_one = np.array([1.04, 0.96, 0.88, 0.80])
data_bu_three = np.array([1.3, 1.5, 1.6, 2.0])

data_ul_one = np.array([1.04, .78, .62, .26, 0.00])
data_ul_three = np.array([1.3, 1.5, 1.6, 1.7, 1.8])

bl_three, bl_one= smooth_bootstrap(data_bl_three, data_bl_one, 100)
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

smooth_three = np.append( data_bl_three, data_ul_three)
smooth_one = np.append( data_bl_one, data_ul_one)

for i in range(5):
    smooth_three = np.append(smooth_three, 0.40)
    smooth_one = np.append(smooth_one, 1.32)
for i in range(2):
    smooth_three = np.append(smooth_three, 0.80)
    smooth_one = np.append(smooth_one, 1.26)
    
for i in range(50):
    smooth_three = np.append(smooth_three, 1.30)
    smooth_one = np.append(smooth_one, 1.04)

bl_three, bl_one = smooth_bootstrap2(smooth_three, smooth_one, 100, data_bl_three)
ul_three, ul_one = smooth_bootstrap2(smooth_three, smooth_one, 100, data_ul_three)



smooth_three = np.append( data_bl_three, data_bu_three)
smooth_one = np.append( data_bl_one, data_bu_one)

for i in range(5):
    smooth_three = np.append(smooth_three, 0.40)
    smooth_one = np.append(smooth_one, 1.32)
for i in range(2):
    smooth_three = np.append(smooth_three, 0.80)
    smooth_one = np.append(smooth_one, 1.26)
    
for i in range(50):
    smooth_three = np.append(smooth_three, 1.30)
    smooth_one = np.append(smooth_one, 1.04)

bu_three, bu_one = smooth_bootstrap2(smooth_three, smooth_one, 100, data_bu_three)

### markers 

color_count = -1

color_count += 1
ax.scatter(data_bl_three,  data_bl_one, zorder=1, color=colours_markers[color_count],  marker=shapes[color_count], s=marker_size)

color_count += 1
ax.scatter( data_bu_three, data_bu_one, zorder=1, color=colours_markers[color_count],  marker=shapes[color_count], s=marker_size)

color_count += 1
ax.scatter( data_ul_three, data_ul_one, zorder=1, color=colours_markers[color_count],  marker=shapes[color_count], s=marker_size)

ax.scatter( 1.30, 1.04, zorder=2, color='r',  marker='*', s=1250)

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
    bl_three,
    ul_three,
    0,
    0,
    bl_one,
    ul_one,
    0,
    2)
ax.add_patch(first_polygon) 
ax.text( .50, .67, 'Liquid', fontsize=40 )
second_polygon = create_polygon( 
   bl_three, 
   bu_three,
   max_x,
   min_x,
   bl_one,
   bu_one,
   max_y,
   max_y,
   0)
ax.add_patch(second_polygon) 
ax.text( 1.37, 1.26, 'Biaxial', fontsize=40 )
second_polygon = create_polygon( 
   ul_three,
   max_x,
   bu_three[::-1],
   [],
   ul_one,
   min_y,
   bu_one[::-1],
   [],
   1)
ax.add_patch(second_polygon) 
ax.text( 1.70, 0.49, 'Uniaxial', fontsize=40 )
###

###labels
ax.tick_params(axis='x', pad=x_tick_pad)
ax.tick_params(axis='y', pad=y_tick_pad)

ax.set_xlabel(x_label_text, fontsize=75, labelpad=x_label_pad)
ax.set_ylabel(y_label_text, fontsize=75, rotation=0, labelpad=y_label_pad)

 
plt.xticks(np.linspace(min_x, max_x, 5))
plt.xticks(np.array([0.00, 0.25, 0.50, 0.75, 1.00, 1.25, 1.50, 1.75, 2.00]))
plt.yticks(np.linspace(min_y, max_y, 5))
plt.yticks(np.array([0.00, 0.25, 0.50, 0.75, 1.00, 1.25, 1.50]))
 
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