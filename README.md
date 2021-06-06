This code is developed to assist in weightlifting training data analysis.  To build and install, follow the setuptools documentation.  A minimal build will be
`python -m build`
A minimal install will be
`pip install /path/to/<package>-<release>.whl`
where <package>-<release> will need to be replaced with the package name and release version.

USE
---
The usage and help info can be obtained from `plotss -h`.

It takes as input the dbBackup.csv files created from the Starting Strength Official App.  An optional input is the notefile, which is a json file listing various notes you would like to add to the plot, such as marking achievements or injuries.  The form is:
{
    'YYYY-MM-XX': 'LABEL1',
    'YYYY-MM-XX': 'LABEL2'
}

The output will be png files, which will just replace the extension of the input file with '.png'.  You can plot multiple csv files at once, provided they have unique names.
