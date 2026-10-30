import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import os
import urllib.request
import random
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from numpy import trapezoid
from scipy.signal import argrelmin
from scipy.stats import binned_statistic as binstat
import seaborn as sns
# Global Variables
Area = 2.0 #m**2
baseurl = 'https://gml.noaa.gov/aftp/data/radiation/baseline/spo'
InputPath = '../../../DataFolder'
OutputPath = 'PlotsFolder/'


# import panel data function
def Import_Panel_Data(year, day):
    input_1 = year
    input_2 = day
    # --------REAL PANEL DATA-------------
    #Read the CSV files based on user input
    file_101 = pd.read_csv(f"{InputPath}/spo_dev101_{input_1}_{input_2}.csv",delimiter=',')
    file_103 = pd.read_csv(f"{InputPath}/spo_dev103_{input_1}_{input_2}.csv",delimiter=',')
    
    # Rename the Device ID column to voltage and Voltage to Current
    file_101.rename(columns = {'Device ID': 'V', 'Voltage': 'A'}, inplace=True)
    file_103.rename(columns = {'Device ID': 'V', 'Voltage': 'A'}, inplace=True) # There is a mismatch in the file so voltage column contains current and Device ID contains voltage
    
    # Each file has the data for more than just the day it is. We want to remove these extra dataS
    
    def date2num(date_str): # Renamed 'date' to 'date_str' to avoid confusion with the datetime.date object
        # 26 # first conver the xxxx-xx-xx format to date(xxxx, xx, xx)
    
        # You can skip splitting the string and go directly to parsing:
        date_object = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # 29 # return the day of the year (%j) as an integer
        # The strftime method returns a string, so we convert it to an integer.
        return int(date_object.strftime('%j'))
    # print(f'DEBUG: {input_2}')
    date = file_101['Date']
    NumberDate = date.apply(date2num)
    mask_to_keep =  NumberDate <= int(input_2)
    file_101 = file_101[mask_to_keep]
    # print(f'DEBUG: {mask_to_keep}')
    # print(f'DEBUG: {NumberDate}')
    
    date = file_103['Date']
    NumberDate = date.apply(date2num)
    mask_to_keep = NumberDate <= int(input_2)
    file_103 = file_103[mask_to_keep]
    
    #Extract time, voltage and current data
    
    time_101 = file_101['Time']
    voltage_101 = file_101['V'] 
    current_101 = file_101['A'] 
    
    time_103 = file_103['Time']
    voltage_103 = file_103['V'] 
    current_103 = file_103['A'] 
    
    power_101 = voltage_101 * current_101
    power_103 = voltage_103 * current_103
    # -----------------------------

    # print(f'len(power_101) = {len(power_101)}')
    return voltage_101, current_101, voltage_103, current_103, time_101, time_103



power_101_full = []
voltage_101_full = []
current_101_full = []
time_101_full = []

power_103_full = []
voltage_103_full = []
current_103_full = []
time_103_full = []

for year in [25,26]:

    power_101_data = []
    voltage_101_data = []
    current_101_data = []
    time_101_data = []

    power_103_data = []
    voltage_103_data = []
    current_103_data = []
    time_103_data = []


    Day_Range2025 = np.arange(334, 366, 1)
    Day_Range2026 = [f"{i:03d}" for i in range(1, 26)]
    if year == 25:
        Day_Range = Day_Range2025
    if year == 26:
        Day_Range = Day_Range2026
    for day in Day_Range:
        # print()
        # print()
        # print(day)
        try:
            voltage_101, current_101, voltage_103, current_103, time_101, time_103 = Import_Panel_Data(year, day)
            print('loaded')


            power_101 = voltage_101*current_101

            power_103 = voltage_103*current_103

            if len(voltage_101) <= 2880:
                difference = 2880 - len(voltage_101)
                for i in np.arange(0,difference,1):
                    voltage_101 = np.pad(voltage_101, (1, 0), constant_values=np.nan)


            if len(current_101) <= 2880:
                difference = 2880 - len(current_101)
                for i in np.arange(0,difference,1):
                    current_101 = np.pad(current_101, (1, 0), constant_values=np.nan)


            if len(time_101) <= 2880:
                difference = 2880 - len(time_101)
                for i in np.arange(0,difference,1):
                    time_101 = np.pad(time_101, (1, 0), constant_values='')



            if len(current_103) <= 2880:
                difference = 2880 - len(current_103)
                for i in np.arange(0,difference,1):
                    current_103 = np.pad(current_103, (1, 0), constant_values=np.nan)


            if len(voltage_103) <= 2880:
                difference = 2880 - len(voltage_103)
                for i in np.arange(0,difference,1):
                    voltage_103 = np.pad(voltage_103, (1, 0), constant_values=np.nan)


            if len(time_103) <= 2880:
                difference = 2880 - len(time_103)
                for i in np.arange(0,difference,1):
                    time_103 = np.pad(time_103, (1, 0), constant_values='')

            power_101_data.append(power_101)
            voltage_101_data.append(voltage_101)
            current_101_data.append(current_101)
            time_101_data.append(time_101)

            power_103_data.append(power_103)
            voltage_103_data.append(voltage_103)
            current_103_data.append(current_103)
            time_103_data.append(time_103)


        except:
            print('failed to load')

            power_101 = np.full(2880,np.nan)
            current_101 = np.full(2880,np.nan)
            voltage_101 = np.full(2880,np.nan)
            time_101 = np.full(2880,'')

            power_103 = np.full(2880,np.nan)
            current_103 = np.full(2880,np.nan)
            voltage_103 = np.full(2880,np.nan)
            time_103 = np.full(2880,'')


            power_101_data.append(power_101)
            voltage_101_data.append(voltage_101)
            current_101_data.append(current_101)
            time_101_data.append(time_101)

            power_103_data.append(power_103)
            voltage_103_data.append(voltage_103)
            current_103_data.append(current_103)
            time_103_data.append(time_103)



    power_101_full.append(np.concatenate(power_101_data))
    voltage_101_full.append(np.concatenate(voltage_101_data))
    current_101_full.append(np.concatenate(current_101_data))
    time_101_full.append(np.concatenate(time_101_data))

    power_103_full.append(np.concatenate(power_103_data))
    voltage_103_full.append(np.concatenate(voltage_103_data))
    current_103_full.append(np.concatenate(current_103_data))
    time_103_full.append(np.concatenate(time_103_data))

power_101_total = np.concatenate((power_101_full))
voltage_101_total = np.concatenate((voltage_101_full))
time_101_total = np.concatenate((time_101_full))

power_103_total = np.concatenate((power_103_full))
voltage_103_total = np.concatenate((voltage_103_full))
time_103_total = np.concatenate((time_103_full))

number_of_days = len(np.concatenate((Day_Range2026, Day_Range2025)))
bins_per_day = 1
bins = number_of_days*bins_per_day

counts_power_101, bin_edges_101 = np.histogram(power_101_total, bins = bins)
counts_power_103, bin_edges_103 = np.histogram(power_103_total, bins = bins)

# time_x = np.concatenate((time_101_total))

bin_indices = np.linspace(0, len(time_103_total) - 1, bins, dtype=int)
time_x_binned = time_101_total[bin_indices]
# print(time_x)
# print(len(time_x))
# print(len(counts_power_101))
# print(len(bin_edges))
# print(bins)
# print(len(power_101_total))
# print(len(time_x)/bins)


# make the timestamps
# print(len(counts_power_101))
x_data = np.arange(0, len(counts_power_101), 1)
x_data = np.arange(0, len(counts_power_103), 1)
start_time = time_101_total[0]
start_date = Day_Range2025[0]

end_time = time_101_total[-1]
end_time = time_103_total[-1]
end_date = Day_Range2026[-1]

def generate_even_datetimes(start_date, start_time, end_date, end_time, n):
    '''Vibecoded cuz this is annoying'''
    # Combine start and end date/time strings
    start_str = f"{start_date} {start_time}"
    end_str = f"{end_date} {end_time}"
    
    # Parse into datetime objects
    start_dt = datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
    end_dt = datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S")
    
    if n <= 1:
        return [start_dt.strftime("%Y-%m-%d %H:%M:%S")]
    
    # Divide the total timespan by (n - 1) to get the exact interval step
    step = (end_dt - start_dt) / (n - 1)
    
    # Generate the list (Date first, then Time)
    datetime_list = [
        (start_dt + i * step).strftime("%Y-%m-%d %H:%M:%S") 
        for i in range(n)
    ]
    
    return datetime_list

# print(end_date)
# date_string_start = f"{2025}-{start_date}"
# date_obj_start = datetime.strptime(date_string_start, "%Y-%j")
# date_string_end = f"{2026}-{end_date}"
# date_obj_end = datetime.strptime(date_string_end, "%Y-%j")
print(start_time)
time_x = generate_even_datetimes('2025-12-11', '00:00:30', '2026-01-26', '05:08:30', len(x_data))

print(time_x)

# print(len(time_x_binned))
sns.set_style('darkgrid')
# print(len(counts_power_101))
# print(len(x_data))
# plt.scatter(x_data, counts_power_101, s = 1)
# plt.scatter(x_data, counts_power_103, s = 1)
power_101_total = np.asarray(power_101_total, dtype=float)
power_103_total = np.asarray(power_103_total, dtype=float)
mean_101, bin_edges_101, bin_number_101 = binstat(np.arange(0,len(power_101_total), 1), power_101_total, statistic = np.nanmean, bins = bins)
mean_103, bin_edges_103, bin_number_103 = binstat(np.arange(0,len(power_103_total)), power_103_total, statistic = np.nanmean, bins = bins)
# bin_size_101 = bin_edges_101[1] - bin_edges_101[0]
# bin_size_103 = bin_edges_103[1] - bin_edges_103[0]
# plt.figure(figsize=(20,4.8))
fig, (ax1, ax2, ax3) = plt.subplots(nrows = 3, ncols = 1, figsize=(20,10), sharex = True)
# ax1.plot(x_data, mean_101, label = 'panel 101', color = '#5e03fc')
# ax2.plot(x_data, mean_103, label = 'panel 103', color = '#5e03fc')

ax1.scatter(x_data, mean_101, label = 'panel 101', color = '#5e03fc')
ax2.scatter(x_data, mean_103, label = 'panel 103', color = '#5e03fc')
# plt.xticks(np.linspace(0,len(time_x_binned), 13))

# time_x_binned = np.where(time_x_binned == '', np.nan, time_x_binned)
number_shown = 10
entry_shown = int(len(x_data)/number_shown)



# get sky coverage 
november_2025_sky_coverage = [3]
december_2025_sky_coverage = [2,7,6,7,3,3,2,2,1,0,3,7,1,2,5,4,6,4,2,5,3,5,6,2,3,7,7,4,0,2,7]
january_2026_sky_coverage = [5,7,8,8,4,4,1,2,1,1,3,8,5,2,1,2,6,8,7,3,4,2,5,5,4,6,7,6,6,3,0]
# correct for day range
combined_cloud = np.concatenate((november_2025_sky_coverage, december_2025_sky_coverage, january_2026_sky_coverage[:25]))
print(len(combined_cloud))
print(len(x_data))
ax3.scatter(x_data, combined_cloud)
ax3.set_ylabel('Cloud level /8', fontsize = 15)
# fig.tight_layout(pad=2.0) 

# ax1.set_xticks(x_data[::entry_shown], time_x[::entry_shown], rotation = 0, fontsize = 7)
ax1.set_xticklabels(['']*len(x_data[::entry_shown]))
ax2.set_xticklabels(['']*len(x_data[::entry_shown]))
ax3.set_xticks(x_data[::entry_shown], time_x[::entry_shown], rotation = 20, fontsize = 7)
fig.suptitle('Solar Panel Power Mean Per Day', fontsize = 20)
ax1.legend()
ax2.legend()
ax3.set_xlabel('time', fontsize = 15)
# ax1.set_xlabel('time')
ax1.set_ylabel('Power [w]', fontsize = 15)
ax2.set_ylabel('Power [w]', fontsize = 15)
ax1.set_ylim(0,300)
ax2.set_ylim(0,300)
# plt.tick_params(axis = 'x', rotation = 0, labelsize = 5)
# plt.xlim(0,len(time_x)-1)
# ax1.grid(True)
# ax2.grid(True)
# ax3.grid(True)
ax1.grid(visible=True, which='both', axis='both', linestyle='-', linewidth=1, color='white', alpha=0.5)
ax1.set_axisbelow(True)

ax2.grid(visible=True, which='both', axis='both', linestyle='-', linewidth=1, color='white', alpha=0.5)
ax2.set_axisbelow(True)

ax3.grid(visible=True, which='both', axis='both', linestyle='-', linewidth=1, color='white', alpha=0.5)
ax3.set_axisbelow(True)

plt.savefig('full_test_power_per_day.png')
plt.show()






