#!/usr/bin/env python

import spear
tool = spear.tools.IVecTool

# 2/ GMM Training
n_gaussians = 512
iterk = 25
iterg_train = 25
convergence_threshold = 1e-5
end_acc = 0.0001
var_thd = 0.0001
update_weights = True
update_means = True
update_variances = True
norm_KMeans = True

# 3/ IVector Training
rt = 400
relevance_factor = 4
max_iterations = 25
n_iter_enrol = 1

# 4/ JFA Enrolment and scoring
iterg_enrol = 1
variance_threshold = 0.0001
relevance_factor = 4
responsibilities_threshold = 0

# 5/ PLDA training
subspace_dimension_pca = None
PLDA_TRAINING_ITERATIONS = 200 # Maximum number of iterations for the EM loop
PLDA_TRAINING_THRESHOLD = 1e-3 # Threshold for ending the EM loop

SUBSPACE_DIMENSION_OF_F = 50 # Size of subspace F
SUBSPACE_DIMENSION_OF_G = 50 # Size of subspace G
variance_flooring = 1e-5

INIT_SEED = 0 # seed for initializing
INIT_F_METHOD = 'BETWEEN_SCATTER'
INIT_G_METHOD = 'WITHIN_SCATTER'
INIT_S_METHOD = 'VARIANCE_DATA'

# These parameters were removed in Bob2
#INIT_F_RATIO = 1
#INIT_G_RATIO = 1
#INIT_S_RATIO = 1

# 6/ LDA training
# LDA subspace; if not set, LDA subspace is not truncated
LDA_SUBSPACE_DIMENSION = 200

# cosine scoring? Default plda_scoring
COSINE_SCORING = False


