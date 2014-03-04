#!/usr/bin/python
# vim: set fileencoding=utf-8 :
# @author: Manuel Guenther <Manuel.Guenther@idiap.ch>
# @date: Fri Nov 16 16:21:24 CET 2012
#
# Copyright (C) 2011-2013 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import argparse
import os

import sys
import bob
import numpy

# for plotting
import matplotlib
import matplotlib.pyplot as mpl
from matplotlib.backends.backend_pdf import PdfPages
# enable LaTeX interpreter
matplotlib.rc('text', usetex=True)
matplotlib.rc('font', family='serif')
# increase the default font size
matplotlib.rc('font', size=18)
matplotlib.rcParams['xtick.major.pad'] = 20


def command_line_options():
  """This function defines and parses the command line arguments that are accepted by this script."""
  # create argument parser
  parser = argparse.ArgumentParser()

  # add command lien arguments, with description and default values
  parser.add_argument('-s', '--scores', required = True, nargs = '+', help = 'The score files of the systems to be evaluated')
  parser.add_argument('-n', '--names', required = True, nargs = '+', help = 'The short names of the systems (must be the same lenght as --scores)')
  parser.add_argument('-c', '--columns', default = 4, type=int, help = 'The number of columns the legend will use')
  parser.add_argument('-D', '--det', default = 'det.pdf',help = 'The file containing the DET plots')

  # parse and return the given command line arguments
  return parser.parse_args()


def process_file(score_file):
  res.append(bob.measure.load.split_four_column(files_sorted[i]))
  return res


def main():
  # get command line arguments
  args = command_line_options()
  assert len(args.scores) == len(args.names)

  # read dev score file
  results = {}
  for n, score_file in enumerate(args.scores):
    results[args.names[n]] = bob.measure.load.split_four_column(score_file)


  # plot the results
  det = PdfPages(args.det)

  # list of FAR (for the ROC)
  density, lowest_power = 4, -4
  far_list = [10.**(x/float(density)) for x in range(lowest_power*density,1)]
  det_list = [1e-3, 5e-3, 1e-2, 2e-2, 5e-2, 1e-1, 2e-1, 4e-1, 5e-1]

  cmap = mpl.cm.get_cmap(name='hsv')
  colors = [cmap(i) for i in numpy.linspace(0, 1.0, len(results)+1)]
  #colors = [(.5,0,0,1), (1,0,0,1), (0,0.5,0,1), (0,1,0,1), (0,0,0.5,1), (0,0,1,1)]
  markers = ('-d', '-o', '-x', '-s', '-*', '-h', '-^', '-v', '-<', '->', '-p', '-+', '-D', '-H', '-1', '-2', '-3', '-4')

  # plot DET curves of the different systems
  figure = mpl.figure(figsize=(8.2,8))
  for n in range(len(results)):
    name = args.names[n]
    frr, far = bob.measure.det(results[name][0], results[name][1], 1000)
    mpl.plot(far, frr, markers[n], color = colors[n], lw=3, ms=10, mew=3, mec = colors[n], label=name, markevery=50)

  ticks = [bob.measure.ppndf(d) for d in det_list]
  labels = [("%.5f" % (d*100)).rstrip('0').rstrip('.') for d in det_list]
  mpl.xticks(ticks, labels, fontsize=18, va='baseline')
  mpl.yticks(ticks, labels, fontsize=18)
  mpl.axis((ticks[0], ticks[-1], ticks[0], ticks[-1]))

  mpl.xlabel('False Acceptance Rate (\%)', fontsize=22)
  mpl.ylabel('False Rejection Rate (\%)', fontsize=22)
  mpl.grid(True, color=(0.3,0.3,0.3))
  legend_handle = mpl.legend(ncol=args.columns, loc=9, prop={'size':16}, bbox_to_anchor=(0.5, 1.15), title='Comparison between systems') # put the title you want here
  det.savefig(figure,bbox_inches='tight',pad_inches=0.25, bbox_extra_artists=[legend_handle])

  det.close()


if __name__ == '__main__':
  main()
