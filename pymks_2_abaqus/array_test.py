import numpy as np
from scipy.io import savemat



sample_size = 3
n_samples = 1 * [sample_size]
arr = np.zeros((3, 21, 21, 21))
for i in range(0, 10):
    arr[:, i*2 + 1, i, i] = 1

#dataset_flattened = np.transpose(arr, (1, 2, 3, 0)).astype(bool)
#mat_dict = {'data': dataset_flattened.reshape(-1, sum(n_samples))}
mat_dict = {'data': arr}
savemat('data_test.mat', mat_dict)
