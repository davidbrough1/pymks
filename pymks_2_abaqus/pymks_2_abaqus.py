import numpy as np
from scipy.io import savemat
from pymks.datasets import make_microstructure
sample_size = 10
n_samples = 6 * [sample_size]
size = (71, 71, 71)
elastic_modulus = (1.3, 75)
poissons_ratio = (0.42, .22)
macro_strain = 1.
n_phases = 2
grain_size = [(30, 1, 1), (1, 30, 1), (1, 1, 30), (5, 1, 1), (1, 5, 1), (1, 1, 5)]
# These are for long and short - How do I do continuous
v_frac = [(0.8, 0.2), (0.7, 0.3), (0.6, 0.4), (0.5, 0.5), (0.3, 0.7), (0.4, 0.6)]
per_ch = 0.1
seed=10

dataset = []
for v_f in v_frac:
    _dataset = np.concatenate([make_microstructure(n_samples=samps, size=size, grain_size=grains, seed=seed, volume_fraction=v_f, percent_variance=per_ch) for samps, grains in zip(n_samples, grain_size)])
    dataset.append(_dataset)
dataset = np.concatenate(dataset)
print dataset.shape

# Creating continuous fibers
con_stack = np.zeros((sample_size * 6, size[0], size[1], size[2]))

sam = np.zeros(size)
ran_slice = sam[1, :, :]
for x in range(con_stack.shape[0]):
    for frac in range(30, 90, 10):
        #print "fraction", float(frac) / 100
        ran_slice = np.random.choice((0, 1), size=(size[1], size[2]),
                                 p=[1 - (float(frac) / 100),
                                    (float(frac) / 100)])
        #print "Actual fraction", float(sum(sum(ran_slice))) / (size[1] * size[2])
        for i in range(size[0]):
            sam[i, :, :] = ran_slice
        con_stack[x, :, :, :] = sam


print con_stack.shape
dataset = np.concatenate([dataset, con_stack], axis=0)
print dataset.shape
dataset_flattened = np.transpose(dataset, (1, 2, 3, 0)).astype(bool)
print sum(n_samples*6), sum(n_samples, sample_size*6)
mat_dict = {'data': dataset_flattened.reshape(-1, sum(n_samples*6) + sample_size*6)}
savemat('data.mat', mat_dict)
