#!/home/ericsmith/anaconda3/bin/python
'''
Workout data and plotting from Starting Strength Official App data.
@author: Eric S. Smith <esmith4422@gmail.com>
'''

# Python
import os
# Anaconda
import pandas as pd
from argparse import ArgumentParser
# Local
from plot_weightlifting.plotstartingstrength import plot_db


def main():
    """ Main function """
    # Add Injuries
    description = '''Plots Starting Strength Official App data.  
        Output png will be named after database file'''
    parser = ArgumentParser(description=description)
    
    help_msg = 'filepath to Starting Strength Official App database file'
    parser.add_argument('filename', help=help_msg, nargs='+')
    help_msg = 'filepath to notes file.  File holds notes for plot.'
    parser.add_argument('--notefile', help=help_msg)

    args = parser.parse_args()

    success = []
    failure = []
    print(f'Executing {__file__}')
    for arg in args.filename:
        fname = os.path.abspath(arg)
        ret = plot_db(fname, notefile=args.notefile)
        if ret == 0:
            success.append(fname)
        elif ret == 1:
            failure.append([fname, 1])
        elif ret == 2:
            failure.append([fname, 2])
        else:
            raise('plot_db: Unknown return status')

    print(f'Executing {__file__} complete!')

    # Summary
    print(f'Successfully processed files:')
    [print(f'\t{_}->{os.path.splitext(_)[0]}.png') for _ in success]

    print(f'Skipped files:')
    err_dict = {
        1: 'Parse failure',
        2: 'File missing XDATA column',
    }

    for _, err in failure:
        print(f'\t{_}')
        print(f'\t\tError Code {err}: {err_dict[err]}')


if __name__ == '__main__':
    main()

