import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


class MKSProcessStructureModel(LinearRegression):
    """docstring for MKSProcessStructureModel"""
    def __init__(self, n_steps, ar_order=1, *args):
        self.ar_order = ar_order
        self.n_steps = n_steps
        super(MKSProcessStructureModel, self).__init__(*args)

    def _add_autoregressive_terms(self, X):
        """
        """
        ar_list = range(1, self.ar_order + 1)
        X_ar = np.zeros((X.shape[0], X.shape[1] * (self.ar_order)))
        for ar in ar_list:
            for i in range(1, ar + 1):
                s0 = slice(i - 1, i)
                s1 = slice(X[0].shape[0] * (ar - 1),  X[0].shape[0] * ar)
                X_ar[s0, s1] = X[0]
                X_ar[ar:, s1] = X[:-ar]
        return X_ar, X

    def fit(self, X, y=None):
        """
        Args:
            X: (n_samples, n_steps, n_PCs)
        """
        X_ar, y = self._fit_prep_X(X)
        super(MKSProcessStructureModel, self).fit(X_ar, y)

    def predict(self, X, y=None):
        """

        Args:
            X: (n_samples, n_PCs)
        """
        if X[0].shape[0] != self.ar_order:
            raise RuntimeError('initial values must be as long as ar_order')
        n_features = self.coef_.shape[0]
        ar_range = range(n_features, n_features * self.ar_order + 1,
                         self.ar_order)
        ar_range = [None] + ar_range + [None]
        ar_slices = [slice(i, j) for i, j in zip(ar_range[:-1], ar_range[1:])]
        y_shape = (self.n_steps, n_features)
        y = np.zeros(y_shape)
        _X = np.zeros((len(X), self.n_steps, X[0].shape[-1]))
        for ii, x in enumerate(X):
            _X[ii, :self.ar_order] = x
        X_ar, y = self._pred_prep_X(_X)
        for xx, yy in zip(X_ar, y):
            for i in range(self.n_steps):
                yy[i] = super(MKSProcessStructureModel, self).predict(xx[i])
                for j, s in enumerate(ar_slices[:-1]):
                    try:
                        if j <= i:
                            xx[i + 1, s] = yy[i - j]
                    except:
                        pass
        return y

    def _fit_prep_X(self, X):
        """
        """
        slice_indx = np.insert(np.cumsum([i.shape[0] for i in X]), 0, 0)
        slices = [slice(i, j) for i, j in zip(slice_indx[:-1], slice_indx[1:])]
        X_ar = np.zeros((slice_indx[-1], X[0].shape[-1] * self.ar_order))
        y = np.zeros((slice_indx[-1], X[0].shape[-1]))
        for s, x in zip(slices, X):
            X_ar[s], y[s] = self._add_autoregressive_terms(x)
        return X_ar, y

    def _pred_prep_X(self, X):
        """
        """
        slices = [slice(0, i.shape[0]) for i in X]
        X_ar = np.zeros((len(X), self.n_steps, X[0].shape[-1] * self.ar_order))
        y = np.zeros((len(X), self.n_steps, X[0].shape[-1]))
        for ii, s, x in zip(range(len(X)), slices, X):
            X_ar[ii][s], y[ii][s] = self._add_autoregressive_terms(x)
        return X_ar, y

    def score(self, X, y=None):
        """
        """
        n_steps = self.n_steps
        y_pred = []
        for x in X:
            self.n_steps = len(x)
            y_pred.append(self.predict(x[:self.ar_order][None]))
        print [i.shape for i in y_pred]
        y_pred = np.concatenate(y_pred).reshape((-1, X[0].shape[-1]))
        X = np.concatenate(X).reshape((-1, X[0].shape[-1]))
        self.n_steps = n_steps
        return r2_score(y_pred, X)


if __name__ == '__main__':
    Pmodel = MKSProcessStructureModel(10, ar_order=2)
    X = np.arange(45).reshape((3, 5, 3))
    Pmodel.fit(X)
    print X[:, 0][:, None].shape
    print Pmodel.predict(X[:, 0][:, None])
