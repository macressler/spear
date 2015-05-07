#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Manuel Guenther <Manuel.Guenther@idiap.ch>

import bob.io
import bob.learn.em
import numpy

from . import ISVTool
import logging
logger = logging.getLogger("bob.c++")
logger.setLevel(logging.INFO)
logger.propagate = True

class JFATool (ISVTool):
  """Tool for computing Unified Background Models and Gaussian Mixture Models of the features and project it via JFA"""

  def __init__(self, setup):
    """Initializes the local UBM-GMM tool with the given file selector object"""
    # call base class constructor
    ISVTool.__init__(self, setup)

    self.m_subspace_dimension_of_u = self.m_config.ru
    self.m_subspace_dimension_of_v = self.m_config.rv
    self.m_jfa_training_iterations = self.m_config.n_iter_train
    self.m_jfa_enroll_iterations = self.m_config.n_iter_enrol


  #######################################################
  ################ JFA training #########################
  
  def train_enroler(self, train_files, enroler_file):
    # create a JFABasemachine with the UBM from the base class
    self.m_jfabase = bob.learn.em.JFABase(self.m_ubm, self.m_subspace_dimension_of_u, self.m_subspace_dimension_of_v)

    # load GMM stats from training files
    gmm_stats = self.__load_gmm_stats_list__(train_files)

    # train the JFA
    trainer = bob.learn.em.JFATrainer()
    bob.learn.em.train_jfa(trainer, self.m_jfabase, gmm_stats, self.m_jfa_training_iterations, rng=bob.core.random.mt19937(self.m_init_seed))

    # Save the JFA base AND the UBM into the same file
    self.m_jfabase.save(bob.io.base.HDF5File(enroler_file, "w"))



  #######################################################
  ################## JFA model enroll ####################
  def load_enroler(self, enroller_file):
    """Reads the UBM model from file"""
    # now, load the JFA base, if it is included in the file
    self.m_jfabase = bob.learn.em.JFABase(bob.io.base.HDF5File(enroller_file))
    # add UBM model from base class
    self.m_jfabase.ubm = self.m_ubm

    self.m_machine = bob.learn.em.JFAMachine(self.m_jfabase)
    self.m_trainer = bob.learn.em.JFATrainer()


  def read_feature(self, feature_file):
    """Reads the projected feature to be enrolled as a model"""
    return bob.learn.em.GMMStats(bob.io.base.HDF5File(str(feature_file)))


  def enroll(self, enroll_features):
    """Enrolls a GMM using MAP adaptation"""

    self.m_trainer.enroll(self.m_machine, enroll_features, self.m_jfa_enroll_iterations)
    # return the resulting gmm
    return self.m_machine


  ######################################################
  ################ Feature comparison ##################
  def read_model(self, model_file):
    """Reads the JFA Machine that holds the model"""
    machine = bob.learn.em.JFAMachine(bob.io.base.HDF5File(model_file))
    machine.jfa_base = self.m_jfabase
    return machine

  def read_probe(self, feature_file):
    return self.read_feature(feature_file)

  def score(self, model, probe):
    """Computes the score for the given model and the given probe"""
    return model.log_likelihood(probe)

  def score_for_multiple_probes(self, model, probes):
    """This function computes the score between the given model and several given probe files."""
    # TODO: Check if this is correct
    utils.warn("This function needs to be verified!")
    raise NotImplementedError('Multiple probes is not yet supported')
    #scores = numpy.ndarray((len(probes),), 'float64')
    #model.forward(probes, scores)
    #return scores[0]


