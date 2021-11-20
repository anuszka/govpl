import pandas as pd
import sys
# sys.path.append('/home/ochab/koronawirus_PAN/gov.pl')
# import helper_functions as hf
from helper_functions import getfile, unzip, display_all_col, was_modified_today
import eurostat
import icu
import time
import datetime
import os
# from copy import deepcopy
import glob
import chardet

def csvs2df(data_dir):
    # merges all csv files in directory into one data frame
    all_files = sorted(glob.glob(os.path.join(data_dir, "*.csv")) ,key=str.lower)
    dfs = []
    for f in all_files: 
        raw_data = open(f, 'rb').read()
        encoding=chardet.detect(raw_data)['encoding']
        if encoding == 'Windows-1252':
            encoding = 'Windows-1250'
        df_from_file = pd.read_csv(f,encoding = encoding,sep=';')   
        if 'stan_rekordu_na' not in df_from_file.columns:
            filename_date = f.strip(data_dir)
            year = int(filename_date[0:4])
            month = int(filename_date[4:6])
            day = int(filename_date[6:8]) - 1
            if day == 0:
                day = 31
                month = 12
                year = year - 1
            df_from_file['stan_rekordu_na'] = datetime.date(year=year,month=month,day=day) 
        dfs.append(df_from_file) 
    concatenated_df   = pd.concat(dfs, ignore_index=True)
    return concatenated_df

def make_nuts_df(data_dir, nuts_names_file):
    # Make data frame: NUTS codes of any level and corresponding names of NUTS units
    nuts_df = pd.read_excel(data_dir +'/'+nuts_names_file)
    return nuts_df

def make_nuts2PL_df(nuts_df):
    # Make data frame: 
    # First row: NUTS code for Poland (country)
    # Other rows: NUTS2 codes for Poland (voivodships)
    nuts2PL_df = nuts_df[
        (nuts_df['NUTS code'].str.contains('PL')) 
        & (nuts_df['NUTS level'] == 2) 
        & (~nuts_df['NUTS code'].str.contains('PLZZ'))
    ]
    nuts2PL_df=nuts2PL_df.append(nuts_df[nuts_df['NUTS code']=='PL'])
    return nuts2PL_df



def df2dict(keys_column, values_column):
    # Convert data frame to dictionary
    return dict(zip(keys_column, values_column))

def make_nuts2PLdict(data_dir, nuts_names_file):
    # Make dictionary: {'NUTS code':'Name of NUTS unit'}
    # First row: NUTS code for Poland (country)
    # Other rows: NUTS2 codes for Poland (regions)
    nuts_df = make_nuts_df(data_dir, nuts_names_file)
    nuts2PL_df = make_nuts2PL_df(nuts_df)
    nuts2PL_df['Name of NUTS unit'] = nuts2PL_df['Name of NUTS unit'].str.title() # Capitalize all words
    nuts2PLdict = df2dict(nuts2PL_df['NUTS code'], nuts2PL_df['Name of NUTS unit'])
    return nuts2PLdict

def locale_sorted(list, locale):
    # Sort alphabetically according to locale
    collator = icu.Collator.createInstance(icu.Locale(locale))
    list = sorted(list, key=collator.getSortKey)
    return(list)


def make_voi_list(data_dir, nuts_names_file):
    nuts2PLdict = make_nuts2PLdict(data_dir, nuts_names_file)
    to_pop = ['PL91', 'PL92', 'PL']
    for key in to_pop:
        nuts2PLdict.pop(key)    
    voi_list = list(nuts2PLdict.values())
    voi_list = locale_sorted(voi_list, 'pl_PL.UTF-8')
    return voi_list


def get_eurostat_population_df():
    df_pop = eurostat.get_data_df('demo_r_d2jan')
    return df_pop

def select_by_NUTS2(df_pop, nuts2PLdict):
    # Slice df_pop to get rows only for NUTS2 codes from the Poland NUTS2 codes dictionary
    df_pop_nuts2 = df_pop[(df_pop['geo\\time'].isin(nuts2PLdict.keys())) 
        & (df_pop['sex'] == 'T')
        & (df_pop['age'] == 'TOTAL')
    ].copy() # Make a copy after slicing before adding a new column
    return df_pop_nuts2

def insert_col_full_region_names(df_pop_nuts2, nuts2PLdict):
    # Insert column with full names of the NUTS2 regions for Poland
    df_pop_nuts2['region name'] = df_pop_nuts2['geo\\time'].map(nuts2PLdict)
    df_pop_nuts2=df_pop_nuts2.reset_index(drop=True)
    return df_pop_nuts2

def make_row_Mazowieckie(df_pop_nuts2):
    # Make new row for Mazowieckie (Warsaw + Mazowsze region: PL91+PL92)
    mazowieckie = df_pop_nuts2[(df_pop_nuts2['geo\\time'] == 'PL91') | (df_pop_nuts2['geo\\time']=='PL92')].sum(numeric_only=True)
    newrow = pd.DataFrame(mazowieckie).transpose()
    newrow.insert(0, 'unit' , 'NR')
    newrow.insert(1, 'sex' , 'T')
    newrow.insert(2, 'age' , 'TOTAL')
    newrow.insert(3,'geo\\time', 'PL91+PL92')
    newrow.insert(len(newrow.columns), 'region name', 'Mazowieckie')
    return newrow

def make_voivodships_df(df_pop_nuts2):
    # Make voivodships data frame:
    # Remove last two rows, PL91 and PL92, and replace by the new row, PL91+PL92
    newrow = make_row_Mazowieckie(df_pop_nuts2)
    df_pop_woj = df_pop_nuts2.iloc[:-2 , :].append(newrow).reset_index(drop=True)
    df_pop_woj['region name'] = df_pop_woj['region name'].str.title() # Capitalize all words
    return df_pop_woj


def make_voi_pop_dict(data_dir, nuts_names_file, df_pop):
    # Make dictionary of voivodships and their populations (first row is Poland total)
    df_pop_nuts2 = make_pop_nuts2_df(data_dir, nuts_names_file, df_pop)
    df_pop_woj = make_voivodships_df(df_pop_nuts2)
    woj_pop_dict = dict(zip(df_pop_woj['region name'],df_pop_woj['2020']))
    return woj_pop_dict 


    

def get_govpl_data_df(url, data_dir, file):
    file_path = data_dir+'/'+file
    if (not os.path.exists(file_path))  or (not was_modified_today(data_dir+'/'+file)):
        print("Downloading gov.pl data")
        getfile(url, file_path)
        unzip(data_dir, file)
    print("Merging gov.pl files to data frame")
    df = csvs2df(data_dir) # Multiple csv files to single dataframe
    return df
    

def format_gov_df(df):
    # Format the governmental data frame
    df['Data'] = pd.to_datetime(df['stan_rekordu_na'])
    df.loc[(df['wojewodztwo'] == 'Cały kraj'), 'wojewodztwo'] = 'Polska' # Replace 'Cały kraj' with 'Polska'
    df['wojewodztwo'] = df['wojewodztwo'].str.title() # Capitalize all words
    return df

def insert_col_voi_pop(df, woj_pop_dict):
    # Add new column with voivodship population
    df['Ludność'] = df['wojewodztwo'].map(woj_pop_dict) 
    return df

def make_pop_nuts2_df(data_dir, nuts_names_file, df_pop):
    nuts2PLdict = make_nuts2PLdict(data_dir, nuts_names_file)
    df_pop_nuts2 = select_by_NUTS2(df_pop, nuts2PLdict)
    df_pop_nuts2 = insert_col_full_region_names(df_pop_nuts2, nuts2PLdict)
    return df_pop_nuts2

# def insert_col_cases1e5(df):
#     df['Przypadki na 100 tys. mieszkańców'] = 1e5*df['liczba_przypadkow'] / df['Ludność']
#     return df

# def insert_col_deaths1e5(df):
#     df['Zgony na 100 tys. mieszkańców'] = 1e5*df['zgony'] / df['Ludność']
#     return df


def format_gov_df_ins_cols(df, woj_pop_dict):
    print("Formatting gov.pl data frame")
    df = format_gov_df(df)
    print("Inserting voivodship population column into gov.pl data frame")
    df = insert_col_voi_pop(df, woj_pop_dict)
    # df = insert_col_cases1e5(df)
    # df = insert_col_deaths1e5(df)
    return df

def make_df_pop(eurostat_pop_data_path):
    print("Making Eurostat population data frame")
    if os.path.exists(eurostat_pop_data_path):
        print("Eurostat data file exists. Making data frame from file.")
        df_pop = pd.read_csv(eurostat_pop_data_path,index_col=0)
    else:
        print("Eurostat data file does not exist. Downloading from Eurostat.")
        df_pop = get_eurostat_population_df()
        df_pop.to_csv(eurostat_pop_data_path)
        df_pop = pd.read_csv(eurostat_pop_data_path,index_col=0) # Jest tu jakiś problem z formatem nazwy kolumny 2020. Chwilowe obejście
    return df_pop



def make_gov_voi_pop_df(url, file, data_dir, nuts_names_file, formatted_data_path, eurostat_pop_data_path):
    print("Making formatted gov.pl data frame")
    
    df_pop = make_df_pop(eurostat_pop_data_path)
    voi_pop_dict = make_voi_pop_dict(data_dir, nuts_names_file, df_pop)

    if os.path.exists(formatted_data_path) and was_modified_today(formatted_data_path):
        print("Today's gov.pl data file exists. Reading from file.")
        df = pd.read_csv(formatted_data_path,index_col=0)
    else:
        print("Today's gov.pl data file does not exist.")
        df = get_govpl_data_df(url, data_dir, file)
        format_gov_df_ins_cols(df, voi_pop_dict)
        df.to_csv(formatted_data_path)

    df['Data'] = pd.to_datetime(df['Data']) # Sanitizing # Jedne poprawia, ale inne stają się NaT
    
    print("Making formatted voivodship list")
    voi_list = make_voi_list(data_dir, nuts_names_file)    
    
    return df, voi_list



