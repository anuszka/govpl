"""
Pandas helpers
--------------

read_dataframe: read data frame

hist_to_df: Export numpy.histogram to pandas data frame

"""

import pandas as pd
import numpy as np
from loghelpers import *




@logger("Read file:",show_first_argument=True)
def read_dataframe(file, sep=','):
    df = pd.read_csv(file,low_memory=False, sep=sep)
    return df


def hist_to_df(dfcol, bins, density=True):
    h= np.histogram(dfcol, bins=bins, density=density)
    dfh = pd.DataFrame(h).transpose()
    dfh=dfh[reversed(dfh.columns)]
    dfh.columns=['bin_min','value']
    return dfh