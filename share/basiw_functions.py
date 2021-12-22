import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import datetime
from share.helper_functions import was_modified_today, display_all

#------------------------------------------------------------------------------


class RawDf:
    df : pd.DataFrame
    def __init__(self, df : pd.DataFrame) -> None:
        self.df=df
#------------------------------------------------------------------------------

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

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------

class CEZvacformat:
    image_dir : str
    data_dir : str
    data_file_vac : str
    teryt_file : str
    path_vac : str
    path_teryt : str
    _dfv_raw : RawDf
    _df_teryt_raw : RawDf
    df_woj : pd.DataFrame
    teryt_dict : dict
    dfv : pd.DataFrame

    def __init__(self,
        image_dir : str,
        url_vac : str,
        data_dir : str,
        # data_file_vac : str,
        teryt_file : str
        ) -> None:

        self.image_dir=image_dir
        self.data_dir=data_dir
        # self.data_file_vac=data_file_vac
        self.teryt_file=teryt_file
        self.path_vac = url_vac
        # self.path_vac = os.sep.join([self.data_dir,self.data_file_vac])
        self.path_teryt = os.sep.join([self.data_dir,self.teryt_file])
        self.read_data()
        self.make_teryt_dict()
        self.dfv = self.format_df(self._dfv_raw)
        return


    def read_data(self) -> None:
        # if was_modified_today(path_vac):
        #     print('Data up to date')
        #     dfv = pd.read_csv(path_vac, encoding = 'cp1250', sep = ';')
        #     dfc = pd.read_csv(path_cases, encoding = 'cp1250', sep = ';')
        # else:
        #     print('Old data, need to download new data!')
        self._dfv_raw = RawDf(pd.read_csv(self.path_vac, encoding = 'iso8859_2', sep = ';',low_memory=False))
        self._df_teryt_raw= RawDf(pd.read_csv(self.path_teryt, sep = ';'))
        return
        
    def make_teryt_dict(self) -> None:
        self.df_woj = self._df_teryt_raw.df.query('NAZWA_DOD == "województwo"')[['WOJ', 'NAZWA']]
        self.df_woj['NAZWA'] = self.df_woj['NAZWA'].str.title()
        self.df_woj.index = self.df_woj.pop('WOJ')
        self.teryt_dict = self.df_woj.to_dict()['NAZWA']
        return

    def format_df(self, df_raw : RawDf) -> pd.DataFrame:
        df = df_raw.df.copy(deep=True)
        df['Województwo'] = df['wojewodztwo_teryt']
        df['Województwo'].replace(self.teryt_dict, inplace=True)
        return df

    

#------------------------------------------------------------------------------





def get_popwoj_df() -> pd.DataFrame:
    dfpopwoj = pd.read_csv('/home/ochab/koronawirus_PAN/gov.pl/bitbucket/govpl/GUS/gus_data/wojewodztwa_ludnosc_plec_30.06.2021_GUS.csv')
    dfpopwoj['Województwo'] = dfpopwoj['Województwo'].str.title()
    dfpopwoj.drop(['TERYT'], axis='columns', inplace=True)
    dfpopwoj.index = dfpopwoj['Województwo']
    dfpopwoj.drop(['Województwo'], axis='columns' , inplace = True)
    return dfpopwoj



#------------------------------------------------------------------------------



def prepare_df(deaths_df: pd.DataFrame, from_date : datetime.date) -> pd.DataFrame:
    base_df = deaths_df[deaths_df['data_rap_zgonu'] >= pd.to_datetime(from_date)]

    dfpopwoj  = get_popwoj_df()
    dfpopwoj = dfpopwoj[['Ludność']]


    df = base_df.groupby('Województwo').sum()
    df.drop(['wiek', 'teryt_pow', 'teryt_woj'], axis = 'columns' , inplace=True)
    df['Województwo'] = df.index
    df['Ludność'] = df['Województwo'].replace(dfpopwoj.to_dict()['Ludność'])
    df

    Q = f'(w_pelni_zaszczepiony == "N")'

    df1 = base_df.query(Q).groupby('Województwo').sum()
    df1.drop(['wiek', 'teryt_pow', 'teryt_woj'], axis = 'columns' , inplace=True)
    df['Zgony nie w pełni zaszczepionych'] = df1

    Q = f'(w_pelni_zaszczepiony == "T")'

    df1 = base_df.query(Q).groupby('Województwo').sum()
    df1.drop(['wiek', 'teryt_pow', 'teryt_woj'], axis = 'columns' , inplace=True)
    df['Zgony w pełni zaszczepionych'] = df1




    df['Zgony nie w pełni zaszczepionych na 100 tys. mieszkańców'] = df['Zgony nie w pełni zaszczepionych'] / df['Ludność'] * 1e5
    df['Zgony w pełni zaszczepionych na 100 tys. mieszkańców'] = df['Zgony w pełni zaszczepionych'] / df['Ludność'] * 1e5

    df = df.sort_values(['Zgony nie w pełni zaszczepionych na 100 tys. mieszkańców'], ascending=False)
    return df

#------------------------------------------------------------------------------
   
def plot_df(from_date : datetime.date, df : pd.DataFrame, image_dir : str) -> pd.DataFrame:
    nie = 'Zgony nie w pełni zaszczepionych na 100 tys. mieszkańców'
    tak = 'Zgony w pełni zaszczepionych na 100 tys. mieszkańców'

    fig = go.Figure(
        data=[
            go.Bar(
                name = nie, 
                x=df['Województwo'], 
                y=df[nie], 
                offsetgroup=1,
                text = df[nie]
                ),
            go.Bar(
                name = tak, 
                x=df['Województwo'], 
                y=df[tak], 
                offsetgroup=2,
                text = df[tak]
                )
        ]
    )

    fig.update_traces(
        texttemplate='%{text:2.1f}', 
        textposition='outside',
        )

    fig.update_layout(
        barmode='group', 
        width=800, 
        height=500,
        title = "Liczba zgonów na COVID-19 w województwach na 100 tys. mieszkańców<br>\
        w podziale na w pełni zaszczepionych i nie w pełni zaszczepionych<br>(Od " + str(from_date) + ")",
        yaxis_title="Liczba zgonów na 100 tys.",
        legend_title="",
        uniformtext_minsize=6, 
        uniformtext_mode='show',
        legend=dict(
            y=-0.5,
            xanchor="center",
            x=0.5
            ),
        title_xanchor='center',
        title_x = 0.5,
        title_font_size=16
        )
    fig.update_xaxes(tickangle=33)
    fig.show()
    fig.write_image(os.sep.join([image_dir, 'zgony_szczep_1e5_woj_od'+str(from_date)+'.jpg']), scale=4)
    return


#------------------------------------------------------------------------------




def group_by(base_df: pd.DataFrame, x_col: str, x_col_name : str, denominator_df: pd.DataFrame, denominator_col : str) -> pd.DataFrame:
   df = base_df.groupby(x_col).sum()
   df.drop(['wiek', 'teryt_pow', 'teryt_woj'], axis = 'columns' , inplace=True)
   df = pd.concat([df,denominator_df[denominator_col]], axis='columns')
   # display(df)

   Q = f'(w_pelni_zaszczepiony == "N")'

   df1 = base_df.query(Q).groupby(x_col).sum()
   df1.drop(['wiek', 'teryt_pow', 'teryt_woj'], axis = 'columns' , inplace=True)
   df['Zgony nie w pełni zaszczepionych '  + denominator_col] = df1
   
   
   Q = f'(w_pelni_zaszczepiony == "T")'

   df1 = base_df.query(Q).groupby(x_col).sum()
   df1.drop(['wiek', 'teryt_pow', 'teryt_woj'], axis = 'columns' , inplace=True)
   df['Zgony w pełni zaszczepionych '  + denominator_col] = df1
   df[x_col]=df.index
   df.rename({x_col : x_col_name}, axis=1, inplace=True)
   return df
#------------------------------------------------------------------------------
 
 
def prepare_df2(deaths_df: pd.DataFrame, x_col: str, x_col_name : str, denominator_df: pd.DataFrame, denominator_col : str, from_date : datetime.date) -> pd.DataFrame:
   base_df = deaths_df[deaths_df['data_rap_zgonu'] >= pd.to_datetime(from_date)]

   df = group_by(base_df, x_col, x_col_name, denominator_df, denominator_col)
   # display(df)

   df['Zgony nie w pełni zaszczepionych ' + denominator_col + ' na 100 tys. ' + denominator_col] =\
      df['Zgony nie w pełni zaszczepionych '  + denominator_col].to_numpy() / df[denominator_col].to_numpy() * 1e5
   # display(df)
   
   df['Zgony w pełni zaszczepionych ' + denominator_col + ' na 100 tys. ' + denominator_col] =\
      df['Zgony w pełni zaszczepionych '  + denominator_col].to_numpy() / df[denominator_col].to_numpy() * 1e5

   # df = df.sort_values(['Zgony nie w pełni zaszczepionych na 100 tys. mieszkańców'], ascending=False)
   return df
   

#------------------------------------------------------------------------------


def plot_df2(
    x_col : str, 
    denominator_col : str, 
    title : str, 
    filename_str : str,  
    from_date : datetime.date, 
    df : pd.DataFrame, 
    image_dir : str,
    width=800, 
    height=500,
    legend_y=-0.25
    ) -> pd.DataFrame:

    nie = 'Zgony nie w pełni zaszczepionych ' + denominator_col + ' na 100 tys. ' + denominator_col
    tak = 'Zgony w pełni zaszczepionych ' + denominator_col + ' na 100 tys. ' + denominator_col

    fig = go.Figure(
        data=[
            go.Bar(
                name = nie, 
                x=df[x_col], 
                y=df[nie], 
                offsetgroup=1,
                text = df[nie]
                ),
            go.Bar(
                name = tak, 
                x=df[x_col], 
                y=df[tak], 
                offsetgroup=2,
                text = df[tak]
                )
        ]
    )

    fig.update_traces(
        texttemplate='%{text:2.1f}', 
        textposition='outside',
        )

    fig.update_layout(
        barmode='group', 
        width=width, 
        height=height,
        title = title , #"Liczba zgonów " + denominator_col + " na COVID-19 " + title_str + " na 100 tys. "+ denominator_col +
        # "<br>w podziale na w pełni zaszczepionych i nie w pełni zaszczepionych<br>(od " + str(from_date) + ")",
        yaxis_title="Liczba zgonów na 100 tys.",
        legend_title="",
        uniformtext_minsize=6, 
        uniformtext_mode='show',
        legend=dict(
            y=legend_y,
            xanchor="center",
            x=0.5
            ),
        title_xanchor='center',
        title_x = 0.5,
        title_font_size=16
        )
    fig.update_xaxes(tickangle=33)
    fig.show()
    fig.write_image(os.sep.join([image_dir, 'zgony_szczep_1e5_'+ filename_str + '_od'+str(from_date)+'.jpg']), scale=4)
    return

#------------------------------------------------------------------------------




def plot_df3(df : pd.DataFrame, image_dir : str, filename : str) -> None:
    tak = 'Współistniejące [%]'
    nie = 'Brak współistniejących [%]'

    fig = go.Figure(
        data=[
            go.Bar(
                name = tak, 
                x=df['Województwo'], 
                y=df[tak], 
                offsetgroup=1,
                text = df[tak]
                ),
            go.Bar(
                name = nie, 
                x=df['Województwo'], 
                y=df[nie], 
                offsetgroup=2,
                text = df[nie]
                )
        ]
    )

    fig.update_traces(
        texttemplate='%{text:2.1f}', 
        textposition='outside',
        )

    fig.update_layout(
        barmode='group', 
        width=800, 
        height=500,
        title = "Procent zgonów na COVID-19 w województwach w podziale na występowanie chorób współistniejących<br>(Od 14.07.2021)",
        yaxis_title="Procent zgonów",
        legend_title="",
        uniformtext_minsize=8, 
        uniformtext_mode='show',
        legend=dict(
            y=-0.5,
            xanchor="center",
            x=0.5
            ),
        title_xanchor='center',
        title_x = 0.5,
        title_font_size=16
        )
    fig.update_xaxes(tickangle=33)
    fig.show()
    fig.write_image(os.sep.join([image_dir, filename]), scale=4) #zgony_wspolist_4fala.jpg
    return

#------------------------------------------------------------------------------

  
def plot_df4(from_date : datetime.date, df : pd.DataFrame, image_dir : str) -> pd.DataFrame:
    nie = 'Zgony nie w pełni zaszczepionych na 100 tys. mieszkańców'
    tak = 'Zgony w pełni zaszczepionych na 100 tys. mieszkańców'
    vac = 'Wyszczepienie [%]'

    fig = go.Figure(
        data=[
            go.Bar(
                name = nie, 
                x=df['Województwo'], 
                y=df[nie], 
                offsetgroup=1,
                text = df[nie],
                yaxis='y'
                ),
            go.Bar(
                name = tak, 
                x=df['Województwo'], 
                y=df[tak], 
                offsetgroup=2,
                text = df[tak],
                yaxis='y'
                ),
            go.Bar(
                name = vac, 
                x=df['Województwo'], 
                y=df[vac], 
                offsetgroup=3,
                text = df[vac],
                yaxis='y2'
                )
        ],
        layout={
        'yaxis': {'title': "Liczba zgonów na 100 tys."},
        'yaxis2': {'title': "Wyszczepienie [%]", 'overlaying': 'y', 'side': 'right'}
    }
    )

    fig.update_traces(
        texttemplate='%{text:2.1f}', 
        textposition='outside',
        )


    fig.update_layout(
        barmode='group', 
        width=800, 
        height=600,
        title = "Liczba zgonów na COVID-19 w województwach na 100 tys. mieszkańców<br>\
        w podziale na w pełni zaszczepionych i nie w pełni zaszczepionych<br>(Od " + str(from_date) + ")\
        oraz procent wyszczepienia województwa",
        # yaxis_title="Liczba zgonów na 100 tys.",
        legend_title="",
        uniformtext_minsize=6, 
        uniformtext_mode='show',
        legend=dict(
            y=-0.5,
            xanchor="center",
            x=0.5
            ),
        title_xanchor='center',
        title_x = 0.5,
        title_font_size=16
        )
    fig.update_xaxes(tickangle=33)
    fig.update_yaxes(range = [0,80])
    fig.show()
    fig.write_image(os.sep.join([image_dir, 'zgony_szczep_1e5_woj_wyszczep_proc_od'+str(from_date)+'.jpg']), scale=4)
    return


#------------------------------------------------------------------------------
def prepare_df1(deaths_df: pd.DataFrame, from_date : datetime.date, pop_dict : dict) -> pd.DataFrame:
    base_df = deaths_df[deaths_df['data_rap_zgonu'] >= pd.to_datetime(from_date)]

    df = base_df.groupby('Województwo').sum()
    df.drop(['wiek', 'teryt_pow', 'teryt_woj'], axis = 'columns' , inplace=True)
    df['Województwo'] = df.index
    df['Ludność'] = df['Województwo'].replace(pop_dict)


    df1 = base_df[base_df['dawka_ost'].isnull()]
    df1=df1.groupby('Województwo').sum()

    df1.drop(['wiek', 'teryt_pow', 'teryt_woj'], axis = 'columns' , inplace=True)
    df['0 dawek'] = df1

    Q = f'(dawka_ost == "jedna_dawka")'

    df1 = base_df.query(Q).groupby('Województwo').sum()
    df1.drop(['wiek', 'teryt_pow', 'teryt_woj'], axis = 'columns' , inplace=True)
    df['Jedna dawka'] = df1

    Q = f'(dawka_ost == "pelna_dawka")'

    df1 = base_df.query(Q).groupby('Województwo').sum()
    df1.drop(['wiek', 'teryt_pow', 'teryt_woj'], axis = 'columns' , inplace=True)
    df['Pełna dawka'] = df1

    Q = f'(dawka_ost == "przypominajaca")'

    df1 = base_df.query(Q).groupby('Województwo').sum()
    df1.drop(['wiek', 'teryt_pow', 'teryt_woj'], axis = 'columns' , inplace=True)
    df['Przypominająca'] = df1

    Q = f'(dawka_ost == "uzupełniająca")'

    df1 = base_df.query(Q).groupby('Województwo').sum()
    df1.drop(['wiek', 'teryt_pow', 'teryt_woj'], axis = 'columns' , inplace=True)
    df['Uzupełniająca'] = df1
    df['Zgony bez szczepienia, na 100 tys. mieszkańców'] = df['0 dawek'] / df['Ludność'] * 1e5
    df['Zgony po jednej dawce, na 100 tys. mieszkańców'] = df['Jedna dawka'] / df['Ludność'] * 1e5
    df['Zgony po pełnej dawce, na 100 tys. mieszkańców'] = df['Pełna dawka'] / df['Ludność'] * 1e5
    df['Zgony po dawce przypominającej, na 100 tys. mieszkańców'] = df['Przypominająca'] / df['Ludność'] * 1e5
    df['Zgony po dawce uzupełniającej, na 100 tys. mieszkańców'] = df['Uzupełniająca'] / df['Ludność'] * 1e5

    df = df.sort_values(['Zgony bez szczepienia, na 100 tys. mieszkańców'], ascending=False)
    return df
#------------------------------------------------------------------------------

def plot_df1(from_date : datetime.date, df : pd.DataFrame, image_dir : str) -> pd.DataFrame:
    nie = 'Zgony bez szczepienia, na 100 tys. mieszkańców'
    jedna ='Zgony po jednej dawce, na 100 tys. mieszkańców'
    pelna = 'Zgony po pełnej dawce, na 100 tys. mieszkańców'
    przypominajaca = 'Zgony po dawce przypominającej, na 100 tys. mieszkańców'
    uzupelniajaca = 'Zgony po dawce uzupełniającej, na 100 tys. mieszkańców'
    
    fig = go.Figure(
        data=[
            go.Bar(
                name = nie, 
                x=df['Województwo'], 
                y=df[nie], 
                offsetgroup=1,
                # text = df[nie]
                ),
            go.Bar(
                name = jedna, 
                x=df['Województwo'], 
                y=df[jedna], 
                offsetgroup=2,
                # text = df[jedna]
                ),
            go.Bar(
                name = pelna, 
                x=df['Województwo'], 
                y=df[pelna], 
                offsetgroup=3,
                # text = df[pelna]
                ),
            go.Bar(
                name = przypominajaca, 
                x=df['Województwo'], 
                y=df[przypominajaca], 
                offsetgroup=4,
                # text = df[przypominajaca]
                ),
            go.Bar(
                name = uzupelniajaca, 
                x=df['Województwo'], 
                y=df[uzupelniajaca], 
                offsetgroup=5,
                # text = df[uzupelniajaca]
                )
        ]
    )

    # fig.update_traces(
    #     texttemplate='%{text:2.1f}', 
    #     textposition='outside',
    #     )

    fig.update_layout(
        barmode='group', 
        width=800, 
        height=700,
        title = "Liczba zgonów na COVID-19 w województwach na 100 tys. mieszkańców<br>\
        w podziale na ostatnią dawkę szczepionki (Od " + str(from_date) + ")",
        yaxis_title="Liczba zgonów na 100 tys.",
        legend_title="",
        uniformtext_minsize=6, 
        uniformtext_mode='show',
        legend=dict(
            y=-0.5,
            xanchor="center",
            x=0.5
            ),
        title_xanchor='center',
        title_x = 0.5,
        title_font_size=16
        )
    fig.update_xaxes(tickangle=33)
    fig.show()
    fig.write_image(os.sep.join([image_dir, 'zgony_szczep_dawki_1e5_woj_od'+str(from_date)+'.jpg']), scale=4)
    return
#------------------------------------------------------------------------------
