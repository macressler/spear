#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Elie Khoury <Elie.Khoury@idiap.ch>
# Sat Aug 31 16:39:23 CEST 2013
#
# Copyright (C) 2012-2013 Idiap Research Institute, Martigny, Switzerland
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


from setuptools import setup, find_packages

setup(
    name='bob.spear',
    version='1.9.0',
    description='Speaker recognition toolkit',
    url='https://pypi.python.org/pypi/bob.spear',
    license='GPLv3',
    keywords = "Speaker Recognition, Speaker verification, Gaussian Mixture Model, ISV, UBM-GMM, I-Vector, Audio processing, NIST SRE 2012, Database",
    author='Elie Khoury',
    author_email='Elie.Khoury@idiap.ch',
    long_description=open('README.rst').read(),

    # This line is required for any distutils based packaging.
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
   
    
    entry_points={
      'console_scripts': [
        'spkverif_isv.py = spear.script.spkverif_isv:main',
        'spkverif_gmm.py = spear.script.spkverif_isv:main',
        'spkverif_jfa.py = spear.script.spkverif_jfa:main',
        'spkverif_ivector.py = spear.script.spkverif_ivector:main',
        'para_ubm_spkverif_isv.py = spear.script.para_ubm_spkverif_isv:main',
        'para_ubm_spkverif_gmm.py = spear.script.para_ubm_spkverif_isv:main',
        'para_ubm_spkverif_ivector.py = spear.script.para_ubm_spkverif_ivector:main',
        'fusion_llr.py = spear.script.fusion_llr:main',
        'det.py = spear.script.det:main',
        'evaluate.py = facereclib.script.evaluate:main',
#        'manual_vad_conversion.py = spear.script.manual_vad_conversion:main',
        ],
      },


install_requires=[
        "setuptools", # for whatever
        "bob.core",
        "bob.io.base",
        "bob.ap",
        "bob.math",
        "bob.measure",
        "bob.learn.linear",
        "bob.learn.em",
        "bob.db.verification.filelist",
        "bob.db.voxforge",
        "facereclib",
        
    ],


    classifiers = [
      'Development Status :: 4 - Beta',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Natural Language :: English',
      'Programming Language :: Python',
      'Topic :: Scientific/Engineering :: Artificial Intelligence',
      ],
)
