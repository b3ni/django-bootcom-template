
COMPRESS_PRECOMPILERS = (
    ('text/coffeescript', 'coffee --compile --stdio'),
    ('text/less', 'lessc {infile} {outfile}'),
)

COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter'
]

COMPRESS_CSS_FILTERS = [
     'compressor.filters.cssmin.CSSMinFilter'
]
