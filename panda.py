import pandas as pd
import numpy as np
import scipy.optimize as optimization
import math
import scipy
import Image

width = 73
height = 44

time_channel = [0,2,4,6,8,10,20,30,40,103]

def func(x, A, t, y0):
    return A * 2.71828**(-x/t) + y0

df = pd.read_csv('sliced.xls')

mean_cols = df.filter(regex="Mean")

images_arr = np.zeros((len(time_channel),height,width,3))
lifetime_arr = np.zeros((height,width))
#ttb_arr = np.zeros((height,width))

datasets = []
col_number = 0

for column in mean_cols.columns:
    row = 0
    col_number = col_number + 1
    blue_channel = []
    green_channel = []
    red_channel = []
    normalized_channel = []

    while row < mean_cols[column].size:
        if row % 3 == 0:
            red_channel.append(mean_cols[column][row])
        elif row % 3 == 2:
            green_channel.append(mean_cols[column][row])
        elif row % 3 == 1:
            blue_channel.append(mean_cols[column][row])
        row = row + 1
    
    for time in range(len(time_channel)):
        images_arr[time,(col_number-1) % height][(col_number-1) // height][0] = red_channel[time]
        images_arr[time,(col_number-1) % height][(col_number-1) // height][1] = green_channel[time]
        images_arr[time,(col_number-1) % height][(col_number-1) // height][2] = blue_channel[time]
        #print str(time_channel[time]) + ' ' + str(red_channel[time] / (blue_channel[time] + green_channel[time] + red_channel[time]))

    for index in range(len(red_channel)):
        normalized_channel.append(green_channel[index]) #/ (blue_channel[index] + green_channel[index] + red_channel[index]))

    #print normalized_channel

    initial_guess = [0.05,14,0.34]

    try:
        lifetime = optimization.curve_fit(func, time_channel, normalized_channel, initial_guess)[0][1]
        k = 1/lifetime
    except RuntimeError:
        lifetime = 0
        k = 0
        
    if lifetime > 30:
        lifetime = 0
        k = 0
        
    if k > 0.30:
        k = 0.30
        
    lifetime_arr[(col_number-1) % height][(col_number-1) // height] = k

    print str(green_channel[0]) + ', ' + str(k)

for time in range(len(time_channel)):
    scipy.misc.toimage(images_arr[time], cmin=0, cmax=255).resize([width*40, height*40]).save('outfile' + str(time) + '.png')

scipy.misc.toimage(lifetime_arr).resize([width*40, height*40]).save('k.png')
