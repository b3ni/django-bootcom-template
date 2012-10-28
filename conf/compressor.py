# -*- coding: utf-8 -*-

COMPRESS_ENABLED = True

COMPRESS_PRECOMPILERS = (
   ('text/less', 'lessc {infile} {outfile}'),
   ('text/coffeescript', 'coffee --compile --stdio'),
)
