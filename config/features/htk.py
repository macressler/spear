#!/usr/bin/env python

import spear
import numpy

feature_extractor = spear.feature_extraction.HTKFeatures

# Cepstral coefficients Mask
features_mask = numpy.arange(0,60) 


# Normalization
normalizeFeatures = False


