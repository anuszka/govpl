from share.helper_functions import (
    getfile, 
    unzip, 
    xlsx2xls
)
# import govpl_functions as govpl
import pandas as pd
import importlib
import glob
import os
from typing import NamedTuple

class GUSparams(NamedTuple):
    data_dir : str
    img_dir : str
    url : str
    zipfile : str
    zipfile_path : str
    zip_dir : str
    file_prefix : str
    file_prefix_terminal : str 
    file_suffix : str
    libreoffice_cmd : str

def download_if_no_zipfile(params : GUSparams):
    if not os.path.isfile(params.zipfile_path):
        print('Downloading file: ' + params.url)
        getfile(params.url,params.zipfile_path)
    else:
        print(params.zipfile_path + ' exists, so not downloaded')
    return    
    
def unzip_if_not_unzipped(params : GUSparams):    
    if not glob.glob(os.sep.join([params.zip_dir, '*.xlsx'])) and not glob.glob(os.sep.join([params.zip_dir, '*.xls'])):
        print('Unzipping file: ' + params.zipfile)
        unzip(params.data_dir,params.zipfile)
    else:
        print('*.xlsx or *.xls files exist in ' + params.zip_dir + ', so zip file not extracted')
    return

def convert_to_xls_if_not_converted(params : GUSparams):    
    if not glob.glob(os.sep.join([params.zip_dir, '*.xls'])):
        print('Converting *.xlsx to *.xls')
        for year in range(2000,2022):
            file = params.file_prefix_terminal + str(year) + params.file_suffix
            xlsx2xls(params.zip_dir,file, params.libreoffice_cmd, inplace = True)
    else:
        print('*.xls files exist in ' + params.zip_dir + ', so *.xlsx files not converted to *.xls')
    return

def download_unzip_convert_to_xls(params : GUSparams):
    download_if_no_zipfile(params)
    unzip_if_not_unzipped(params)
    convert_to_xls_if_not_converted(params)
    return