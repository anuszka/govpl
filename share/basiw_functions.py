import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import datetime
from share.helper_functions import was_modified_today, display_all
from share.basiw_functions import BASiWformat



class RawDf:
    df : pd.DataFrame
    def __init__(self, df : pd.DataFrame) -> None:
        self.df=df

class BASiWformat:
    image_dir : str
    data_dir : str
    data_file_deaths : str
    data_file_cases : str
    teryt_file : str
    path_deaths : str
    path_cases : str
    path_teryt : str
    _dfd_raw : RawDf
    _dfc_raw : RawDf
    _df_teryt_raw : RawDf
    df_woj : pd.DataFrame
    teryt_dict : dict
    dfd : pd.DataFrame

    def __init__(self,
        image_dir : str,
        data_dir : str,
        data_file_deaths : str,
        data_file_cases : str,
        teryt_file : str
        ) -> None:

        self.image_dir=image_dir
        self.data_dir=data_dir
        self.data_file_deaths=data_file_deaths
        self.data_file_cases=data_file_cases
        self.teryt_file=teryt_file
        self.path_deaths = os.sep.join([self.data_dir,self.data_file_deaths])
        self.path_cases = os.sep.join([self.data_dir,self.data_file_cases])
        self.path_teryt = os.sep.join([self.data_dir,self.teryt_file])
        self.read_data()
        self.make_teryt_dict()
        self.dfd = self.format_df('data_rap_zgonu', self._dfd_raw)
        return


    def read_data(self) -> None:
        # if was_modified_today(path_deaths):
        #     print('Data up to date')
        #     dfd = pd.read_csv(path_deaths, encoding = 'cp1250', sep = ';')
        #     dfc = pd.read_csv(path_cases, encoding = 'cp1250', sep = ';')
        # else:
        #     print('Old data, need to download new data!')
        self._dfd_raw = RawDf(pd.read_csv(self.path_deaths, encoding = 'cp1250', sep = ';',low_memory=False))
        self._dfc_raw= RawDf(pd.read_csv(self.path_cases, encoding = 'cp1250', sep = ';', low_memory=False))
        self._df_teryt_raw= RawDf(pd.read_csv(self.path_teryt, sep = ';'))
        return
        
    def make_teryt_dict(self) -> None:
        self.df_woj = self._df_teryt_raw.df.query('NAZWA_DOD == "województwo"')[['WOJ', 'NAZWA']]
        self.df_woj['NAZWA'] = self.df_woj['NAZWA'].str.title()
        self.df_woj.index = self.df_woj.pop('WOJ')
        self.teryt_dict = self.df_woj.to_dict()['NAZWA']
        return

    def format_df(self, col : str, df_raw : RawDf) -> pd.DataFrame:
        df = df_raw.df.copy(deep=True)
        df[col] = pd.to_datetime(df[col], format = "%Y-%m-%d")
        df['Województwo'] = df['teryt_woj']
        df['Województwo'].replace(self.teryt_dict, inplace=True)
        return df

    def dfd_from(self, start_date : datetime.date) -> pd.DataFrame:
        return self.dfd[self.dfd['data_rap_zgonu'] >= pd.to_datetime(start_date)]
        