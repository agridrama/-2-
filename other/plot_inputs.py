import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# read csv file
# csv does not contain column names and row numbers
data01 = pd.read_csv('01_4_A.csv', header=None)
data02 = pd.read_csv('02_4_A.csv', header=None)
data04 = pd.read_csv('04_4_A.csv', header=None)
# omit the first 10,000 rows
data01 = data01.iloc[5000:]
data02 = data02.iloc[5000:]
data04 = data04.iloc[5000:]
# adjust the minmum length
min_length = min(len(data01), len(data02), len(data04))
data01 = data01.iloc[:min_length//4]
data02 = data02.iloc[:min_length//4]
data04 = data04.iloc[:min_length//4]
# combine the data
# print(data)
# set column names, input_data, output_data
data01.columns = ['input_ref1', 'input_ref2', 'input_ref3', 'input_ref4', 'input_val1', 'input_val2', 'input_val3', 'input_val4','output_1', 'output_2', 'output_3', 'output_4']
data02.columns = ['input_ref1', 'input_ref2', 'input_ref3', 'input_ref4', 'input_val1', 'input_val2', 'input_val3', 'input_val4','output_1', 'output_2', 'output_3', 'output_4']
data04.columns = ['input_ref1', 'input_ref2', 'input_ref3', 'input_ref4', 'input_val1', 'input_val2', 'input_val3', 'input_val4','output_1', 'output_2', 'output_3', 'output_4']

data = []
data.append(data01)
data.append(data02)
data.append(data04)
# sampling rate is 500 Hz
fs = 500
t = np.arange(0, len(data01)/fs, 1/fs)
# calculate time
# plot input and output data
ds = ["0.1", "0.2", "0.4"]
dtype = ["target", "input", "output"]
plt.figure()
for i in range(3):
  for j in range(3):
    plt.subplot(3, 3, i*3 + j + 1)
    if j == 0:
        plt.plot(t, data[i]['input_ref1'], label='input_ref1')
        plt.ylabel('P / kPa')
    elif j == 1:
        plt.plot(t, data[i]['input_val1'], label='input_val1')
    else:
        plt.plot(t, data[i]['output_1'], label='output_1')
        plt.ylim((90,110))
    if i == 2:
       plt.xlabel('time / s ')
    
    plt.title("d = " + ds[i] + " " + dtype[j])

plt.show()
