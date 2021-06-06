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

    parse_good = []
    parse_bad = []
    print(f'Executing {__file__}')
    for arg in args.filename:
        fname = os.path.abspath(arg)
        try:
            print(f'Plotting {fname}...')
            plot_db(fname, notefile=args.notefile)
            parse_good.append(fname)
            print(f'Plotting {fname} complete!')
        except pd.errors.ParserError:
            print(f'Invalid file: {fname}.  Skipping...')
            parse_bad.append(fname)
        except KeyError:
            print(f'Invalid file: {fname}.  Skipping...')
            parse_bad.append(fname)

    print(f'Executing {__file__} complete!')

    # Summary
    print(f'Successfully processed files:')
    [print(f'\t{_}') for _ in parse_good]

    print(f'Skipped files:')
    [print(f'\t{_}') for _ in parse_bad]


if __name__ == '__main__':
    main()

