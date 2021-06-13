The intent of this program is to analyze training log data for weight lifting. 
This code currently only supports training data in the format as exported from 
the Official Starting Strength App.  The format of such data is a CSV file.  
The required columns are as follows:

 - Date
 - Squat Weight
 - Deadlift Weight
 - Bench Weight
 - Press Weight
 - Power Clean Weight

> note:
> Additional columns will be ignored.

INSTALLATION
------------
To build and install, follow the setuptools documentation.  A minimal build will
be 
```
python -m build
```
A minimal install will be
```
pip install /path/to/<package>-<release>.whl
```
where \<package\>-\<release\> will need to be replaced with the package name 
and release version.

USE
---
The usage and help info can be obtained from `plotss -h`.

It takes as input the dbBackup.csv files created from the Starting Strength 
Official App.  An optional input is the notefile, which is a JSON file listing
various notes you would like to add to the plot, such as marking achievements 
or injuries.  The form is:
```
{
    "YYYY-MM-XX": {"label": 'LABEL1',
                   "ydata": 'YDATA'},
    "YYYY-MM-XX": {"label": 'LABEL2',
                   "ydata": 'YDATA'},
}
```

LABEL will be displayed in the textbox.  YDATA is the exercise in which to
post the textbox next to.  It must match a column header from the training
log.  

> note:
> If no lift matching YDATA occured on the date, then it will use a default
> location to place the textbox.

The output will be png files, which will just replace the extension of the 
input file with '.png'.  You can plot multiple csv files at once, provided 
they have unique names.
