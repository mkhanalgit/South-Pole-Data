import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import binned_statistic as binstat

high_albedo_mount_data = pd.read_csv('septest3.6.csv')
high_albedo_data = pd.read_csv('spo_dev104_26_246.csv')

high_albedo_mount_time = high_albedo_mount_data.iloc[:,0].tolist()
high_albedo_mount_angle = high_albedo_mount_data.iloc[:,1].tolist()

high_albedo_time = np.array(high_albedo_data.iloc[1:,1].tolist())
high_albedo_voltage = np.array(high_albedo_data.iloc[1:,3].tolist())
high_albedo_current = np.array(high_albedo_data.iloc[1:,4].tolist())

# print(high_albedo_voltage)
# print(high_albedo_current)

high_albedo_power = high_albedo_voltage*high_albedo_current

# print(high_albedo_carpark_data)

# print(high_albedo_)
# print(len(high_albedo_time))
# print(len(high_albedo_power))




low_albedo_mount_data = pd.read_csv('septest22.1.csv')
low_albedo_data = pd.read_csv('spo_dev104_26_265.csv')

low_albedo_mount_time = low_albedo_mount_data.iloc[:,0].tolist()
low_albedo_mount_angle = low_albedo_mount_data.iloc[:,1].tolist()

low_albedo_time = np.array(low_albedo_data.iloc[1:,1].tolist())
low_albedo_voltage = np.array(low_albedo_data.iloc[1:,3].tolist())
low_albedo_current = np.array(low_albedo_data.iloc[1:,4].tolist())

# print(low_albedo_voltage)
# print(low_albedo_current)

low_albedo_power = low_albedo_voltage*low_albedo_current


plt.plot(high_albedo_time, high_albedo_power)
plt.xticks(np.linspace(1, len(high_albedo_time), 8), rotation = 45)
plt.show()

plt.plot(low_albedo_time, low_albedo_power)
plt.xticks(np.linspace(1, len(low_albedo_time), 8), rotation = 45)
plt.show()

print(high_albedo_time)
print()
print(high_albedo_mount_time)

# print(len(low_albedo_time))
# print(len(low_albedo_power))

# make the data align

# print(len(low_albedo_time))
# print(len(low_albedo_power))

high_albedo_start_time = '15:52:15'

low_albedo_start_time = '12:47:15'

# print(f'low albedo power = {low_albedo_power}')
# print(type(low_albedo_power))
# print(low_albedo_power.index(low_albedo_start_time))
print(f'low albedo power index \n {np.where(low_albedo_power == low_albedo_start_time)}')
# print(np.where(high_albedo_power == high_albedo_start_time))

# print(low_albedo_power[np.where(low_albedo_power == low_albedo_start_time)])
# print(np.where(high_albedo_power == high_albedo_start_time))


# plt.plot(low_albedo_time[np.where(low_albedo_power == low_albedo_start_time)[0]:], low_albedo_power[np.where(low_albedo_power == low_albedo_start_time)[0]:])
# plt.xticks(np.linspace(1, len(low_albedo_time), 8), rotation = 45)
# plt.show()


print()
print()
print('This')
print()
print(high_albedo_mount_angle)
print()
print(high_albedo_power)

high_albedo_power_binned = binstat(high_albedo_time, high_albedo_power, statistic = 'mean', bins = len(high_albedo_mount_angle))



# plt.plot(high_albedo_mount_angle, high_albedo_power)
#
# plt.show()




