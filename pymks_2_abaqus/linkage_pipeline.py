from sklearn.decomposition import KernelPCA
from scipy.io import loadmat
from sklearn.grid_search import GridSearchCV
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.base import BaseEstimator


class PipelineModel(BaseEstimator):
    def __init__(self, n_components, degree):
        self._pipe = Pipeline([('poly', PolynomialFeatures(degree=degree)),
                               ('regression', LinearRegression())])
        self.degree = degree
        self.n_components = n_components

    @property
    def degree(self):
        return self._degree

    @degree.setter
    def degree(self, value):
        """Setter for the polynomial degree for property_linker.
        """
        self._degree = value
        self._pipe.set_params(poly__degree=value)

    def fit(self, X, y):
        self._pipe.fit(X[:, :self.n_components], y)

    def predict(self, X):
        return self._pipe.predict(X[:, :self.n_components])

    def score(self, X, y):
        return self._pipe.score(X[:, :self.n_components], y)

reducer = KernelPCA(n_components=20, kernel='precomputed')

kernel_files = ['kernel_00.mat', 'kernel_11.mat', 'kernel_01.mat']

kernels = []

for k in kernel_files[:2]:
	dict_kernel = loadmat(k)
	kernels.append(dict_kernel[dict_kernel.keys()[0]][None])

kernel = np.sum(np.concatenate(kernels), axis=0)

pca_scores = reducer.fit_transform(kernel)

fake_stiffness = np.random.random((len(kernel), 1))

model = PipelineModel(n_components=3, degree=3)
params_to_tune = {'degree': np.arange(1, 4), 'n_components': np.arange(2, 8)}
gs = GridSearchCV(model, params_to_tune).fit(pca_scores, fake_stiffness)
print('Order of Polynomial'), (gs.best_estimator_.degree)
print('Number of Components'), (gs.best_estimator_.n_components)
print('R-squared Value'), (gs.score(pca_scores, fake_stiffness))
 
model = gs.best_estimator_