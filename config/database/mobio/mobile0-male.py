#!/usr/bin/env python

import bob.db.verification.filelist

# 0/ The database to use
name = 'mobile0-male'
db = bob.db.verification.filelist.Database('protocols/mobio/mobile0-male/')
protocol = None

wav_input_dir = "PATH/TO/WAV/"
wav_input_ext = ".wav"

