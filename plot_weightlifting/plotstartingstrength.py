'''
Module for plotting Starting Strength Official App database files
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


# Plot columns.  Must match column headers in the db file
XDATA = ['Date']
YDATA = ['Squat Weight', 'Deadlift Weight', 'Bench Weight', 'Press Weight', 
         'Power Clean Weight']


def plot_db(db_fname, notefile=None, figsize=(19.20, 10.80), dpi=100):
    """
    Creates a plot from a starting strength training log database

    Parameters
    ----------
    db_fname : str
        filepath to dbBackup.csv file
    notefile : str, optional
        filepath to json file containing notes
    figsize : 2-tuple of floats, optional
        Resolution values.  Default is 1080p: (19.20, 10.80)
    dpi : int, optional
        dots per inch of plot
    """
    db_basename = os.path.basename(db_fname)
    db_name = os.path.splitext(db_basename)[0]

    # Read in data
    try:
        print(f'\tReading {db_fname}')
        df = pd.read_csv(db_fname, header=0, parse_dates=True, 
                         infer_datetime_format=True)
    except pd.errors.ParserError:
        msg = f'Failed to parse file'
        print(f'{msg}.  Skipping...')
        return msg

    print(f'\tPreprocessing {db_name}...',)
    # Strip leading white spaces from columns
    df.columns = [col.lstrip() for col in df.columns]

    # length of the ' Weight' to subtract for the legend headers
    length = len(YDATA[0].split()[-1]) + 1

    # Convert date strings to dates data
    try:
        df[XDATA[0]] = [mdates.num2date(mdates.datestr2num(_)) for _ in
            df[XDATA[0]]]
    except KeyError:
        msg = f'File is missing {XDATA[0]} column'
        print(f'{msg}.  Skipping...')
        return msg

    # Plot data
    try:
        rcParams['figure.figsize'] = figsize
    except ValueError:
        msg = f'Invalid figsize: {figsize}'
        print(f'{msg}.  Skipping...')
        return msg
    try:
        rcParams['figure.dpi'] = dpi
    except ValueError:
        msg = f'Invalid dpi: {dpi}'
        print(f'{msg}.  Skipping...')
        return msg

    print(f'\tPlotting {db_name}...')
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
    ax.set_title('Strength Progress')
    ax.set_xlabel('Monday Date (YYYY/MM/DD)')
    ax.set_ylabel('Mass (kg)')
    ax2.set_ylabel('Weight (lbs)')

    ax.grid(True)
    ax.legend()

    # Add notes or injuries to canvas.
    injuries = []
    if notefile is not None:
        with open(notefile, 'r') as f1:
            try:
                notes_dict = json.load(f1)
            except json.decoder.JSONDecodeError:
                msg = f'Invalid JSON file: {notefile}.'
                print(f'{msg}.  Skipping...')
                return msg
            except UnicodeDecodeError:
                msg = f'Invalid start byte in file: {notefile}.'
                print(f'{msg}.  Skipping...')
                return msg

        [injuries.append(Injury(k, v['label'], v['ydata'], df, ax)) for k, v in notes_dict.items()]

    bbox = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    for i in range(len(injuries)):
        ax.text(injuries[i].xloc, injuries[i].yloc, injuries[i].label, 
                transform=ax.transAxes, bbox=bbox, rotation=30)

    # Final formatting
    fig.autofmt_xdate()
    fig.tight_layout()

    # Output
    png_fname = f'{db_name}.png'
    print(f'\tSaving {png_fname}...')
    plt.savefig(png_fname)
    print(f'\t{png_fname} saved!')

    return 0


class Injury(object):
    """
    Holds data for a weightlifting injury

    Attributes
    ----------
    date : datetime
        {YYYY-MM-DD}
    label : str
        Text to display on plot
    ydata : str
        Column header text of a lift.  Must match an entry in YDATA.  Places 
        text box above the marker for this lift.
    df : Pandas.DataFrame
        Dataframe holding training data
    ax : Matplotlib.Axes
        Axes object
    """
    def __init__(self, date, label, ydata, df, ax):
        self.date = date
        self.label = label
        self.ydata = ydata
        self.df = df
        self.ax = ax
        self.xloc = 0
        self.yloc = 0
        self.default_yloc = 0.05 
        self.bottom_yloc = 0.01 
        self.top_yloc = 0.90 
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
        if self.ydata.lower() == 'default':
            self.yloc = self.default_yloc
            return
        elif self.ydata.lower() == 'top':
            self.yloc = self.top_yloc
            return
        elif self.ydata.lower() == 'bottom':
            self.yloc = self.bottom_yloc
            return

        injuries_yvals = self.df[df1][self.ydata].values

        # Use default yloc if NaN value for ydata.  
        if pd.isna(injuries_yvals):
            print('\tWarning! '
                  f'Found NaN value for {self.date}.  Defaulting to '
                  f'yloc={self.default_yloc}.')
            self.yloc = self.default_yloc
            return

        bounds = self.ax.get_ybound()
        bounds_delta = bounds[1] - bounds[0]
        epsilon = 0.05 # small amount to shift text boxes from XDATA[0] value
        self.yloc = injuries_yvals / bounds_delta - epsilon

