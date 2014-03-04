# vim: set fileencoding=utf-8 :
#
# Copyright (C) 2013-2014 Idiap Research Institute, Martigny, Switzerland
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

# This program reproduce the results published in the paper: 

# These command line should reproduce the results published in the paper:
# "Spear: An open source toolbox for speaker recognition based on {B}ob, E. Khoury, L. El Shafey, S. Marcel. IEEE Intl. Conf. on Acoustics, Speech and Signal Processing (ICASSP), 2014."


# 1- UBM-GMM + ZT-norm System, Male
bin/spkverif_gmm.py -d config/database/mobio/mobile0-male.py -p config/preprocessing/mod_4hz.py -f config/features/mfcc_60.py -t config/tools/ubm_gmm/ubm_gmm_512G.py -T MOBIO/mobile0-male/ -U MOBIO/mobile0-male/ -b GMM

# 2- ISV System + ZT-norm, Male
bin/spkverif_isv.py -d config/database/mobio/mobile0-male.py -p config/preprocessing/mod_4hz.py -f config/features/mfcc_60.py -t config/tools/isv/isv_512g_u50.py -T MOBIO/mobile0-male/ -U MOBIO2/mobile0-male/ -b ISV

# 3- IVector + Whitening + LNorm + LDA + WCCN + PLDA System, Male
bin/spkverif_ivector.py -d config/database/mobio/mobile0-male.py -z -p config/preprocessing/mod_4hz.py -f config/features/mfcc_60.py -t config/tools/ivec/ivec_512g_t400.py -T MOBIO/mobile0-male/ -U MOBIO/mobile0-male/ -b IVEC_PLDA


# 4- Fusion of the three systems using Logistic Regression
bin/fusion_llr.py -s MOBIO/mobile0-male/GMM/mobile0-male/ztnorm/scores-dev MOBIO/mobile0-male/ISV/scores/mobile0-male/ztnorm/scores-dev MOBIO2/mobile0-male/IVEC_PLDA/scores/mobile0-male/nonorm/scores-dev -t MOBIO/mobile0-male/GMM/mobile0-male/ztnorm/scores-eval MOBIO/mobile0-male/ISV/scores/mobile0-male/ztnorm/scores-eval MOBIO2/mobile0-male/IVEC_PLDA/scores/mobile0-male/nonorm/scores-eval -f fused-scores-dev -g fused-scores-eval


##############################
######### EVALUATION #########

# Plot DET curves of the three systems and their score fusion
bin/det.py -s MOBIO/mobile0-male/GMM/mobile0-male/ztnorm/scores-eval MOBIO/mobile0-male/ISV/scores/mobile0-male/ztnorm/scores-eval MOBIO2/mobile0-male/IVEC_PLDA/scores/mobile0-male/nonorm/scores-eval fused-scores-eval -n GMM ISV i-vectors Fusion

# Compute EER, HTER and minCLLR 
# 1- GMM system
bin/evaluate.py -d MOBIO/mobile0-male/ -U MOBIO/mobile0-male/GMM/scores-dev -e  MOBIO/mobile0-male/GMM/scores-eval -x -c EER

# 2- ISV system
bin/evaluate.py -d MOBIO/mobile0-male/ -U MOBIO/mobile0-male/ISV/scores-dev -e  MOBIO/mobile0-male/ISV/scores-eval -x -c EER

# 3- IVEC-PLDA system
bin/evaluate.py -d MOBIO/mobile0-male/ -U MOBIO/mobile0-male/IVEC-PLDA/scores-dev -e  MOBIO/mobile0-male/IVEC-PLDA/scores-eval -x -c EER

# 4- Fusion system
bin/evaluate.py -d MOBIO/mobile0-male/ -U fused-scores-dev -e  fused-scores-eval -x -c EER
