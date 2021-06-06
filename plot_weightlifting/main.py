#!/home/ericsmith/anaconda3/bin/python
'''
Workout data and plotting from Starting Strength Official App data.
@author: Eric S. Smith <esmith4422@gmail.com>
'''

# Python
import os
import pkg_resources
# Anaconda
import pandas as pd
from argparse import ArgumentParser
# Local
from plot_weightlifting.plotstartingstrength import (plot_db, ERROR_DICT)
from plot_weightlifting.global_vars import (__name__, __version__,
    FIGSIZE_DICT)


def main():
    """ Main function """
    # Argument Parsing
    description = '''Plots Starting Strength Official App data.  
        Output png will be named after database file'''
    parser = ArgumentParser(description=description)
    
    help_msg = 'filepath to Starting Strength Official App database file'
    parser.add_argument('filename', help=help_msg, nargs='+')
    help_msg = 'display version and exit'
    parser.add_argument('-v', '-V', '--version', help=help_msg,
                        action='version', 
                        version=f'{__name__} v{__version__}')
    help_msg = '''figure size of the plot.  Options: 4k, 1080p, 720p, 480p, 
        custom.  Custom usage: --figsize w,h.  w,h are floats representing the
        pixels/100 for width and height.  Default: 1080p: (19.20,10.80)'''
    parser.add_argument('--figsize', help=help_msg)
    parser.add_argument('--dpi', help='dpi of plot.  Default: 100')
    help_msg = 'filepath to notes file.  File holds notes for plot.'
    parser.add_argument('--notefile', help=help_msg)

    args = parser.parse_args()

    # Execute plotter on files
    success = []
    failure = []
    print(f'Executing {__file__}')

    figsize = FIGSIZE_DICT[arg.figsize]
    for arg in args.filename:
        fname = os.path.abspath(arg)
        ret = plot_db(fname, notefile=args.notefile,
                      figsize=figsize,
                      dpi=arg.dpi)
        if ret == 0:
            success.append(fname)
        else:
            failure.append([fname, ret])

    print(f'Executing {__file__} complete!')

    # Print Summary
    print(f'Successfully processed files:')
    [print(f'\t{_}->{os.path.splitext(_)[0]}.png') for _ in success]

    print(f'Skipped files:')

    for _, err in failure:
        print(f'\t{_}')
        print(f'\t\tError Code {err}: {ERROR_DICT[err]}')


if __name__ == '__main__':
    main()

