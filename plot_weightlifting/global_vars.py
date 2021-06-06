'''
Holds global variables for the code
'''


import pkg_resources


__project__ = 'plot_weightlifting'
__name__ = pkg_resources.get_distribution(__project__).project_name
__version__ = pkg_resources.get_distribution(__project__).version

FIGSIZE_DICT = {
    '4k': (38.40, 21.60),
    '1440p': (25.60, 14.40),
    '1080p': (19.20, 10.80),
    '720p': (12.80, 7.20),
    '480p': (6.40, 4.80),
}

