from pymks.tools import draw_components_scatter
from pymks.tools import draw_component_variance
import cPickle as pickle
from scipy.io import loadmat

pca_model = pickle.load(open('pca_model.pkl', 'rb'))
draw_component_variance(pca_model.explained_variance_ratio_)

scores = loadmat('coeff_scores.mat')['scores']
draw_components_scatter([scores[:100, :3], scores[100:, :3]],
                        ['Train', 'Test'])
