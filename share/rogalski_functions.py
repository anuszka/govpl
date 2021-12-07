import pandas as pd
# --------------------------------------------------------------------------    

def format_Rogalski_voi(df : pd.DataFrame, start_row:int, end_row:int) -> pd.DataFrame:
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
    dfc.iloc[0,304:] = dfc.iloc[0,304:] + '.2021'
    pd.to_datetime(dfc.iloc[0,1:], format='%d.%m.%Y')
    dfc.set_index(dfc.columns[0], inplace=True)
    dfc, dfc.columns = dfc[1:] , dfc.iloc[0]
    dfc.index.name = None
    dfc = dfc.apply(pd.to_numeric)
    return dfc

# --------------------------------------------------------------------------    


def format_Rogalski_voi_cases(df : pd.DataFrame) -> pd.DataFrame:
    """
    Format Rogalski data frame, cases

    Args:
        df (pandas.DataFrame):

    Returns:
        pandas.DataFrame
    """
    dfc = format_Rogalski_voi(df, 9, 26)
    return dfc
# --------------------------------------------------------------------------    

def format_Rogalski_voi_deaths(df : pd.DataFrame) -> pd.DataFrame:
    """
    Format Rogalski data frame, deaths

    Args:
        df (pandas.DataFrame):

    Returns:
        pandas.DataFrame
    """
    dfc = format_Rogalski_voi(df, 52, 69)
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
        dfc = format_Rogalski_voi_cases(gsheet_df)
    elif option == 'deaths':
        dfc = format_Rogalski_voi_deaths(gsheet_df)
    return dfc