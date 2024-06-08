import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# read csv file
# csv does not contain column names and row numbers
csv_file = '01_4_B'
# check if normalized data exists
# if not, normalize the data
try:
	data = pd.read_csv(csv_file + '_normalized_3.csv')
except:
  data = pd.read_csv(csv_file + '.csv', header=None)
  # set column names, input_data, output_data
  data.columns = ['input_ref1', 'input_ref2', 'input_ref3', 'input_ref4', 'input_val1', 'input_val2', 'input_val3', 'input_val4','output_1', 'output_2', 'output_3', 'output_4']
  # sampling rate is 500 Hz
  fs = 500
  # calculate time
  t = np.arange(0, len(data)/fs, 1/fs)
  # add time column
  data['time'] = t

  # omit the first 5,000 rows = 10 seconds
  data = data.iloc[5000:]
  # normalize the data, apply different normalization for input and output data
  # mean = 0, std = 1
  data['input_val1'] = (data['input_val1'] - data['input_val1'].mean()) / data['input_val1'].std()
  data['input_val2'] = (data['input_val2'] - data['input_val2'].mean()) / data['input_val2'].std()
  data['input_val3'] = (data['input_val3'] - data['input_val3'].mean()) / data['input_val3'].std()
  data['input_val4'] = (data['input_val4'] - data['input_val4'].mean()) / data['input_val4'].std()
  data['output_1'] = (data['output_1'] - data['output_1'].mean()) / data['output_1'].std()
  data['output_2'] = (data['output_2'] - data['output_2'].mean()) / data['output_2'].std()
  data['output_3'] = (data['output_3'] - data['output_3'].mean()) / data['output_3'].std()
  data['output_4'] = (data['output_4'] - data['output_4'].mean()) / data['output_4'].std()


  # find the index of 1,2,...kth nearest neighbour
  # where k = 10
  k = 10
  neighbours = []
  for i in range(len(data-100)):
      dist = np.sqrt(np.sum((data[['input_val1', 'input_val2', 'input_val3', 'input_val4']].iloc[i].values - data[['input_val1', 'input_val2', 'input_val3', 'input_val4']].values)**2, axis=1))
      # sort the distance and find the kth nearest neighbour
      # keep index of the kth nearest neighbour
      idx = np.argsort(dist)
      neighbours.append(idx[1:k+1])
  print("calculation done")
  # store the index of the kth nearest neighbour
  data['neighbours'] = neighbours
  # write the data to csv file
  # file name is csv_file + '_normalized.csv'
  data.to_csv(csv_file + '_normalized_3.csv', index=False)

# read the normalized data
data = pd.read_csv(csv_file + '_normalized_3.csv')
def str_list_to_list(str_list):
    s = str_list[1:-1].split(' ')
    s = [i for i in s if i != '']
    return [int(i) for i in s]
data['n_list'] = data['neighbours'].apply(str_list_to_list)

# estimate the local jacobian matrix
# using the k nearest neighbour
# and the output data
# y_i(t+1) - y(t+1)) = J_x(t) (x_i(t) - x(t)) + J_y(t) (y_i(t) - y(t)), where J_x(t) and J_y(t) are the local jacobian matrix
# (x_i, y_i) is the ith nearest neighbour
# (x, y) is the current data
# y(t+1) is the output data at time t+1
# x(t) is the input data at time t
# J_x and J_y minimizes the error
# J_x = (X^T X)^-1 X^T Y
# X = [x_i(t) - x(t)], Y = [y_i(t) - y(t)]
# calculate the local jacobian matrix
J_x_list = []
J_y_list = []
for i in range(len(data)-100):
    # find the kth nearest neighbour
    idxs = data.iloc[i]['n_list']
    # "[ 1,2,3,4,5]" -> [1,2,3,4,5]

    # str to list of int
    # if idx includes len(data), remove it
    idx = [j-1 for j in idxs if j < len(data)]
    idx2 = [j for j in idxs if j < len(data)]
    # input data
    X = data.iloc[idx][['input_val1', 'input_val2', 'input_val3', 'input_val4', 'output_1', 'output_2', 'output_3', 'output_4']].astype(float).values - data.iloc[i][['input_val1', 'input_val2', 'input_val3', 'input_val4', 'output_1', 'output_2', 'output_3', 'output_4']].astype(float).values
    # output data
    Y = data.iloc[idx2][['output_1', 'output_2', 'output_3', 'output_4']].values - data.iloc[i+1][['output_1', 'output_2', 'output_3', 'output_4']].values
    # calculate the local jacobian matrix
    J = np.linalg.inv(X.T @ X) @ X.T @ Y
    # separate J_x and J_y
    J_x = J[:4]
    J_y = J[4:]
    # store the local jacobian matrix
    J_x_list.append(J_x)
    J_y_list.append(J_y)
    if i % 1000 == 0:
        print(i)
        print(J_x)

Q = np.identity(4)
LE = 0
# use QR decomposition
for i in range(len(J_y_list)):
  J = J_y_list[i]
  Q, R = np.linalg.qr(J @ Q)
  LE += np.log(np.abs(np.diag(R)))
  if i % 1000 == 0:
      print(i)
      print(LE/(i+1))

LE = LE / len(J_y_list)
print(LE)







