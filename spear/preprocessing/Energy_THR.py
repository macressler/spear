#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Elie Khoury <Elie.Khoury@idiap.ch>
# Fri Aug 30 11:43:14 CEST 2013
#
# Copyright (C) 2012-2013 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Energy-based voice activity detection for speaker recognition"""

import numpy
import bob
import math
from .. import utils
import logging
logger = logging.getLogger("bob.c++")


class Energy_THR:
  """Extracts the Energy"""
  def __init__(self, config):
    self.m_config = config

  def _voice_activity_detection(self, energy_array):
    #########################
    ## Initialisation part ##
    #########################
    #index = self.m_config.energy_mask
    max_iterations = self.m_config.max_iterations
    alpha = self.m_config.alpha
    n_samples = len(energy_array)

    ratio_for_threshold = self.m_config.ratio_for_threshold
    threshold = numpy.mean(energy_array) - numpy.log((100./ratio_for_threshold) * (100./ratio_for_threshold))
    print threshold, numpy.mean(energy_array)
    
    
    label = numpy.array(numpy.ones(n_samples), dtype=numpy.int16)
    
       

    k=0
    for i in range(n_samples):
      if energy_array[i] > threshold:
        label[i]=label[i] * 1
      else:
        label[i]=0
    print("After Energy-based VAD there are %d frames remaining over %d" %(numpy.sum(label), len(label)))
    
    return label


  
  
  def _compute_energy(self, input_file):
    """Computes and returns normalized cepstral features for the given input wave file"""
    
    print("Input wave file: %s" %input_file)
    rate_wavsample = utils.read(input_file)
    
    
    # Set parameters
    wl = self.m_config.win_length_ms
    ws = self.m_config.win_shift_ms
    
    e = bob.ap.Energy(rate_wavsample[0], wl, ws)
    energy_array = e(rate_wavsample[1])
    labels = self._voice_activity_detection(energy_array)
      
    labels = utils.smoothing(labels,10) # discard isolated speech less than 100ms

    
    return labels
    
  
  def __call__(self, input_file, output_file, annotations = None):
    """labels speech (1) and non-speech (0) parts of the given input wave file using Energy"""
    
    labels = self._compute_energy(input_file)
    
    bob.io.save(labels, output_file)
    
