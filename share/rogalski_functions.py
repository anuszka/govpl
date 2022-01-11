"""
Functions for retrieving data from the Rogalski's Google Spreadsheet:
http://bit.ly/covid19-poland
"""
import pandas as pd
# --------------------------------------------------------------------------

def format_rogalski_voi(df : pd.DataFrame, start_row:int, end_row:int) -> pd.DataFrame:
    """
    Format Rogalski data frame

    Args:
        df : pandas.DataFrame
        start_row : int
        end_row : int

    Returns:
        pandas.DataFrame
    """

    dfc = df[start_row:end_row].copy(deep=True)
    dfc.iloc[0,1:304] = dfc.iloc[0,1:304] + '.2020'
    dfc.iloc[0,304:304+365] = dfc.iloc[0,304:304+365] + '.2021'
    dfc.iloc[0,304+365:] = dfc.iloc[0,304+365:] + '.2022'
    dfc.set_index(dfc.columns[0], inplace=True)
    dfc, dfc.columns = dfc[1:] , dfc.iloc[0]
    dfc.index.name = None
    dfc.columns.name = None
    dfc = dfc.apply(pd.to_numeric)
    dfc.columns = pd.to_datetime(dfc.columns, format='%d.%m.%Y')
    dfc = dfc.T
    start_date = pd.to_datetime('2020.01.01')
    end_date = pd.to_datetime('2020.03.03')
    dates = pd.date_range(start_date,end_date)
    df_fill = pd.DataFrame(index = dates, columns=dfc.columns)
    df_fill=df_fill.fillna(0)
    dfc = pd.concat([df_fill,dfc])

    return dfc

# --------------------------------------------------------------------------


def format_rogalski_voi_cases(df : pd.DataFrame) -> pd.DataFrame:
    """
    Format Rogalski data frame, cases

    Args:
        df (pandas.DataFrame):

    Returns:
        pandas.DataFrame
    """
    dfc = format_rogalski_voi(df, 9, 26)
    return dfc
# --------------------------------------------------------------------------
def format_rogalski_voi_deaths(df : pd.DataFrame) -> pd.DataFrame:
    """
    Format Rogalski data frame, deaths

    Args:
        df (pandas.DataFrame):

    Returns:
        pandas.DataFrame
    """
    dfc = format_rogalski_voi(df, 52, 69)
    return dfc

# --------------------------------------------------------------------------

def data_voi_df(gsheet_df : pd.DataFrame, option : str)-> pd.DataFrame:
    """
    Get formatted data frame for regions (voivodships)

    Args:
        gsheet_df : pd.DataFrame
            Rogalski's Google Sheet data frame
        option : str
            = 'cases' or 'deaths'
    Returns:
        pd.DataFrame
    """
    if option == 'cases':
        dfc = format_rogalski_voi_cases(gsheet_df)
    elif option == 'deaths':
        dfc = format_rogalski_voi_deaths(gsheet_df)
    return dfc
