import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# read csv file
# csv does not contain column names and row numbers
ds = [0.1, 0.2, 0.4]
dstrs = ['01', '02', '04']
ranges = ['A', 'B']
for ii in range(3):
  d = ds[ii]
  for jj in range(2):
    name = f'{dstrs[ii]}_4_{ranges[jj]}'
    data = pd.read_csv(name + '.csv', header=None)
    # remove the first 5000 rows of transient states
    data = data.iloc[5000:]
    # set column names, input_data, output_data
    data.columns = ['input_ref1', 'input_ref2', 'input_ref3', 'input_ref4', 'input_val1', 'input_val2', 'input_val3', 'input_val4','output_1', 'output_2', 'output_3', 'output_4']
    # split the data into train and test
    X = data[['output_1', 'output_2', 'output_3', 'output_4']]
    MC = np.zeros(4)
    MCs = np.zeros((4,100*int(2**ii)-1))
    for i in range(1,5):
      y = data[f'input_val{i}']
      X = data[['output_1', 'output_2', 'output_3', 'output_4']]
      for k in range(1,100*int(2**ii)):
        # slide k step
        y = y.shift()
        # remove the first rows
        X = X[1:]
        y = y[1:]

        # split the data into train and test
        X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, train_size=10000)
        # create ridge regression object
        # alpha is the regularization strength, the larger the value, the more the regularization
        reg = Ridge(alpha=0.1)
        # fit the model
        reg.fit(X_train, y_train)

        # predict the input value from the output value
        y_pred = reg.predict(X_test)
        # calculate the covariance of y_pred and y_test
        cov = np.cov(y_pred, y_test)[0, 1]
        # calculate the variance of y_test
        var_test = np.var(y_test)
        # calculate the variance of y_pred
        var_pred = np.var(y_pred)
        # calculate the memory capacity
        MC_k = cov**2 / (var_test*var_pred)
        MC[i-1] += MC_k
        MCs[i-1][k-1] = MC_k
    for i in range(4):
      plt.plot(range(1, 100*int(2**ii)), MCs[i], label=f'input_val{i+1}')
    plt.xlabel('k')
    plt.ylim(0, 1.0)
    plt.ylabel('Memory Capacity at k')
    plt.title(f'Memory Capacity of inputs, ranges = {ranges[jj]}, d = {d}')
    plt.legend()
    # save the figure as a png file
    # please comment out the following line if you do not want to save the figure
    plt.savefig(f'../figs/MC_{name}.png')
    plt.show()
    plt.close()
    
    print(f'Memory Capacity of {name}: {MC}')
