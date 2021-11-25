from share.helper_functions import (
    getfile, 
    unzip, 
    xlsx2xls
)
# import govpl_functions as govpl
import pandas
import importlib
import glob
import os
from typing import NamedTuple

# ==============================================================================

# TODO: [GOV-18] Make a regular class with a constructor
class GUSparams(NamedTuple):
    """
    Parameters for GUS data download and save
    -----------------------------------------
    Inheritance:
        NamedTuple
    Attributes:
        data_dir(str) :
        img_dir(str) :
        url(str) : GUS data file URL
        zipfile(str) : Downloaded GUS data file name (*.zip)
        zipfile_path(str) : zip_dir + zipfile
        zip_dir(str) : Downloaded GUS data file directory
        file_prefix(str) : Here: 'Zgony wedêug tygodni w Polsce_'
        file_prefix_terminal(str) : Here: 'Zgony\ wedêug\ tygodni\ w\ Polsce_'
        file_suffix(str) : Here: '.xlsx'
        libreoffice_cmd(str) : Command to run LibreOffice. Needed for xlsx to xls conversion 
    """
    data_dir : str
    img_dir : str
    url : str
    zipfile : str
    # TODO: [GOV-15] Automatically create zipfile_path within class
    zipfile_path : str
    zip_dir : str
    # TODO: [GOV-16] Set default values of file_prefix, file_prefix_terminal, file_suffix, libreoffice_cmd
    file_prefix : str
    # TODO: [GOV-17] Generate file_prefix_terminal automatically or use it as file_prefix
    file_prefix_terminal : str 
    file_suffix : str
    libreoffice_cmd : str

# ============================================================================

class Analysis:
    """
    Analysis of GUS data 
    -----------------------
    Attributes:
        params(GUSparams) : Parameters for GUS data download and save
    Methods:
        download_if_no_zipfile(self) -> None :
        unzip_if_not_unzipped(self) -> None :
        convert_to_xls_if_not_converted(self) -> None :
        download_unzip_convert_to_xls(self) -> None :
        read_xls_year(self,year) -> pandas.DataFrame:
        format_df(self,df : pandas.DataFrame, year : int) -> pandas.DataFrame:
    """
    # --------------------------------------------------------------------------
    params : GUSparams
    # --------------------------------------------------------------------------
    def download_if_no_zipfile(self) -> None:
        """

        Args:
            None

        Returns:
            None

        """
        if not os.path.isfile(self.params.zipfile_path):
            print('Downloading file: ' + self.params.url)
            getfile(self.params.url,self.params.zipfile_path)
        else:
            print(self.params.zipfile_path + ' exists, so not downloaded')
        return    
    # --------------------------------------------------------------------------    
    def unzip_if_not_unzipped(self) -> None:
        """

        Args:
            None

        Returns:
            None

        """
        if not glob.glob(os.sep.join([self.params.zip_dir, '*.xlsx'])) and not glob.glob(os.sep.join([self.params.zip_dir, '*.xls'])):
            print('Unzipping file: ' + self.params.zipfile)
            unzip(self.params.data_dir,self.params.zipfile)
        else:
            print('*.xlsx or *.xls files exist in ' + self.params.zip_dir + ', so zip file not extracted')
        return
    # --------------------------------------------------------------------------
    def convert_to_xls_if_not_converted(self) -> None:
        """

        Args:
            None
        Returns:
            None

        """
        if not glob.glob(os.sep.join([self.params.zip_dir, '*.xls'])):
            print('Converting *.xlsx to *.xls')

            #TODO: [GOV-19] Set year range as parameter
            for year in range(2000,2022):
            
                file = self.params.file_prefix_terminal + str(year) + self.params.file_suffix
                xlsx2xls(self.params.zip_dir,file, self.params.libreoffice_cmd, inplace = True)
        else:
            print('*.xls files exist in ' + self.params.zip_dir + ', so *.xlsx files not converted to *.xls')
        return
    # --------------------------------------------------------------------------
    def download_unzip_convert_to_xls(self) -> None:
        """

        Args:
            None
        Returns:
            None

        """
        self.download_if_no_zipfile()
        self.unzip_if_not_unzipped()
        self.convert_to_xls_if_not_converted()
        return
    # --------------------------------------------------------------------------
    def read_xls_year(self,year : int) -> pandas.DataFrame:
        """
        Read GUS data file (*.xls from excel_file_path) for the specific year

        Args:
            year (int):

        Returns:
            pandas.DataFrame

        """
        excel_file_path = os.sep.join([self.params.zip_dir, self.params.file_prefix + str(year) + '.xls'])
        df = pandas.read_excel(excel_file_path, 'OGÓŁEM')
        return df
    # --------------------------------------------------------------------------
    def format_df(self,df : pandas.DataFrame, year : int) -> pandas.DataFrame:
        """
        Format GUS data frame for the specific year

        Args:
            df (pandas.DataFrame): GUS data frame, unformatted
            year (int):

        Returns:
            pandas.DataFrame

        """
        df.drop(index=range(0,5),axis=1, inplace=True)
        df.drop(index=6, axis=1, inplace=True)
        df.iloc[0,0]='Wiek zmarłych w latach'
        df.iloc[0,1]='NUTS'
        df.iloc[0,2]='Podregiony'
        df.columns = df.iloc[0]
        df = df[1:]
        df.reset_index(inplace = True, drop = True)
        df.rename_axis('', axis='columns', inplace=True)
        df1 = df.copy(deep=True)
        df1['Rok']=year
        return df1
 
# ============================================================================
