import numpy as np
from scipy.io import savemat
from pymks.datasets import make_microstructure

sample_size = 2
n_samples = 6 * [sample_size]
size = (21, 21, 21)
elastic_modulus = (1.3, 75)
poissons_ratio = (0.42, .22)
macro_strain = 0.001
n_phases = 2
# grain_size = [(40, 2), (10, 2), (2, 40), (2, 10), (2, 30), (30, 2)]
grain_size = [(20, 1, 1), (5, 1, 1), (1, 20, 1), (1, 1, 5), (1, 1, 15), (1, 15, 1)]
v_frac = [(0.8, 0.2), (0.7, 0.3), (0.6, 0.4), (0.5, 0.5), (0.3, 0.7), (0.4, 0.6)]
per_ch = None
seed=10

dataset = np.concatenate([make_microstructure(n_samples=samps,
                              size=size, grain_size=grains, seed=seed,
                               volume_fraction=v_f, percent_variance=per_ch)
                          for samps, grains, v_f in zip(n_samples, grain_size, v_frac)])
print dataset.shape
dataset_flattened = np.transpose(dataset, (1, 2, 3, 0)).astype(bool)
mat_dict = {'data': dataset_flattened.reshape(-1, sum(n_samples))}
savemat('data.mat', mat_dict)
