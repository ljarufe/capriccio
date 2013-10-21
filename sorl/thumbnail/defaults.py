DEBUG = False
BASEDIR = ''
SUBDIR = ''
PREFIX = ''
QUALITY = 85
CONVERT = '/usr/bin/convert'
WVPS = '/usr/bin/wvPS'
EXTENSION = 'jpg'
PROCESSORS = (
    'projectcapriccio.sorl.thumbnail.processors.colorspace',
    'projectcapriccio.sorl.thumbnail.processors.autocrop',
    'projectcapriccio.sorl.thumbnail.processors.scale_and_crop',
    'projectcapriccio.sorl.thumbnail.processors.filters',
)
IMAGEMAGICK_FILE_TYPES = ('eps', 'pdf', 'psd')
