#!/home/ericsmith/anaconda3/bin/python
'''
Workout data and plotting from Starting Strength Official App data.
@author: Eric S. Smith <esmith4422@gmail.com>
'''

# Python
import os
import json

# Anaconda imports
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib import rcParams
from argparse import ArgumentParser


# Plot columns.  Must match column headers in the db file
XDATA = ['Date']
YDATA = ['Squat Weight', 'Deadlift Weight', 'Bench Weight', 'Press Weight', 
         'Power Clean Weight']

# Plot settings.  Uncomment desired settings
#rcParams['figure.figsize'] = 38.40, 21.60 # 4k resolution
#rcParams['figure.figsize'] = 25.60, 14.40 # 1440 resolution
rcParams['figure.figsize'] = 19.20, 10.80 # 1080 resolution
#rcParams['figure.figsize'] = 19.20, 10.80 # custom resolution
rcParams['figure.dpi'] = 100


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
    print(args)

    parse_good = []
    parse_bad = []
    print(f'Executing {__file__}')
    for arg in args.filename:
        fname = os.path.abspath(arg)
        try:
            print(f'Plotting {fname}...')
            run(fname, notefile=args.notefile)
            parse_good.append(fname)
            print(f'Plotting {fname} complete!')
        except pd.errors.ParserError:
            print(f'Invalid file: {fname}.  Skipping...')
            parse_bad.append(fname)

    print(f'Executing {__file__} complete!')

    # Summary
    print(f'Successfully processed files:')
    [print(f'\t{_}') for _ in parse_good]

    print(f'Skipped files:')
    [print(f'\t{_}') for _ in parse_bad]


def run(db_fname, notefile=None):
    """
    Creates a plot from a starting strength training log database

    Parameters
    ----------
    db_fname : str
        filepath to dbBackup.csv file
    notefile : str, optional
        filepath to json file containing notes
    """
    db_basename = os.path.basename(db_fname)

    # Read in data
    print(f'\tReading {db_fname}')
    df = pd.read_csv(db_fname, header=0, parse_dates=True, 
                     infer_datetime_format=True)

    print(f'\tPreprocessing {db_basename}')
    # Strip leading white spaces from columns
    df.columns = [col.lstrip() for col in df.columns]

    # length of the ' Weight' to subtract for the legend headers
    length = len(YDATA[0].split()[-1]) + 1

    # Convert date strings to dates data
    df[XDATA[0]] = [mdates.num2date(mdates.datestr2num(_)) for _ in
        df[XDATA[0]]]

    # Plot data
    #print(f'\tPlotting {db_fname}')
    fig, ax = plt.subplots()

    # Add axis for pounds
    ax2 = ax.twinx()

    for y in YDATA:
        print(f'\t\tPlotting {y}...')
        x1 = df[XDATA[0]]
        y1 = df[y]
        ymask = np.isfinite(y1)
        ax.plot(x1[ymask], y1[ymask], label=y[:-length], marker='.', 
                linestyle='-')

        x2 = x1
        y2 = 2.2 * y1 # convert kg -> pounds
        ax2.plot(x2[ymask], y2[ymask], label=y[:-length], marker='.', 
                 linestyle='-')
        
    # Set tickmarks to Mondays
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0))
    ax.xaxis.set_minor_locator(mdates.DayLocator())

    # Set pound ylabels to align with kg labels
    l = ax.get_ylim()
    l2 = ax2.get_ylim()
    f = lambda x: l2[0]+(x-l[0])/(l[1]-l[0])*(l2[1]-l2[0])
    ticks = f(ax.get_yticks())
    ax2.yaxis.set_major_locator(matplotlib.ticker.FixedLocator(ticks))

    # Set plot labels
    ax.set_title('Starting Strength Progress')
    ax.set_xlabel('Monday Date (YYYY/MM/DD)')
    ax.set_ylabel('Mass (kg)')
    ax2.set_ylabel('Weight (lbs)')

    ax.grid(True)
    ax.legend()

    # Add injuries to canvas.
    injuries = []
    if notefile is not None:
        with open(notefile, 'r') as f1:
            notes_dict = json.load(f1)

        [injuries.append(Injury(k, v, df, ax)) for k, v in notes_dict.items()]

    bbox = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    for i in range(len(injuries)):
        ax.text(injuries[i].xloc, injuries[i].yloc, injuries[i].label, 
                transform=ax.transAxes, bbox=bbox, rotation=30)

    # Final formatting
    fig.autofmt_xdate()
    fig.tight_layout()

    # Output
    png_fname = os.path.splitext(db_basename)[0] + '.png'
    print(f'\tSaving {png_fname}...')
    plt.savefig(png_fname)
    print(f'\tSaving {png_fname} complete!')


class Injury(object):
    """
    Holds data for a weightlifting injury
    """
    def __init__(self, date, label, df, ax):
        self.date = date
        self.label = label
        self.df = df
        self.ax = ax
        self.xloc = 0
        self.yloc = 0
        self._add_hours()
        self.date_start = df[XDATA[0]].iloc[0]
        self.date_end = df[XDATA[0]].iloc[-1]
        self.total_time = mdates.date2num(self.date_end) - \
            mdates.date2num(self.date_start)
        self.get_xloc()
        self.get_yloc()

    def _add_hours(self):
        """Adds the time data for the HH;MM:SS"""
        self.date += ' 00:00:00+00:00'

    def get_xloc(self):
        """Gets the xloc [0, 1] of the injury date"""
        bounds = self.ax.get_xbound()
        bounds_delta = bounds[1] - bounds[0]
        self.xloc = (mdates.datestr2num(self.date) - bounds[0]) / bounds_delta

    def get_yloc(self):
        """Gets the yloc [0, 1] of the injury date"""
        df1 = self.df[XDATA[0]]==self.date
        injuries_yvals = self.df[df1][YDATA[0]].values
        bounds = self.ax.get_ybound()
        bounds_delta = bounds[1] - bounds[0]
        epsilon = 0.05 # small amount to shift text boxes from XDATA[0] value
        self.yloc = injuries_yvals / bounds_delta - epsilon


if __name__ == '__main__':
    main()

