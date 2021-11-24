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
    """
    Parameters for analysis of GUS data

    Args:
        NamedTuple (str): 
            data_dir : Local directory to save data
            img_dir : Local directory to save images
            url : GUS data file URL
            zipfile : 
            zipfile_path : 
            zip_dir : str
            file_prefix : str
            file_prefix_terminal : str 
            file_suffix : str
            libreoffice_cmd : str

    """
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

class Analysis:

    params : GUSparams

    def download_if_no_zipfile(self):
        if not os.path.isfile(self.params.zipfile_path):
            print('Downloading file: ' + self.params.url)
            getfile(self.params.url,self.params.zipfile_path)
        else:
            print(self.params.zipfile_path + ' exists, so not downloaded')
        return    
        
    def unzip_if_not_unzipped(self):    
        if not glob.glob(os.sep.join([self.params.zip_dir, '*.xlsx'])) and not glob.glob(os.sep.join([self.params.zip_dir, '*.xls'])):
            print('Unzipping file: ' + self.params.zipfile)
            unzip(self.params.data_dir,self.params.zipfile)
        else:
            print('*.xlsx or *.xls files exist in ' + self.params.zip_dir + ', so zip file not extracted')
        return

    def convert_to_xls_if_not_converted(self):    
        if not glob.glob(os.sep.join([self.params.zip_dir, '*.xls'])):
            print('Converting *.xlsx to *.xls')
            for year in range(2000,2022):
                file = self.params.file_prefix_terminal + str(year) + self.params.file_suffix
                xlsx2xls(self.params.zip_dir,file, self.params.libreoffice_cmd, inplace = True)
        else:
            print('*.xls files exist in ' + self.params.zip_dir + ', so *.xlsx files not converted to *.xls')
        return

    def download_unzip_convert_to_xls(self):
        self.download_if_no_zipfile()
        self.unzip_if_not_unzipped()
        self.convert_to_xls_if_not_converted()
        return

    def read_xls_year(self,year):
        excel_file_path = os.sep.join([self.params.zip_dir, self.params.file_prefix + str(year) + '.xls'])
        df = pd.read_excel(excel_file_path, 'OGÓŁEM')
        return df

    def format_df(self,df, year):
        df['Rok']=year
        df.drop(index=range(0,5),axis=1, inplace=True)
        df.drop(index=6, axis=1, inplace=True)
        df.iloc[0,0]='Wiek zmarłych w latach'
        df.iloc[0,1]='NUTS'
        df.iloc[0,2]='Podregiony'
        df.columns = df.iloc[0]
        df = df[1:]
        df.reset_index(inplace = True, drop = True)
        df.rename_axis('', axis='columns', inplace=True)
        return df
 
