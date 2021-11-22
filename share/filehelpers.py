"""
File helpers
"""
import os
import glob
from loghelpers import *


        
def add_trailing_slash(directory : str) -> str:
    return os.path.join(directory, '')

@logger("Directory created:",show_first_argument=True)
def check_or_make_dir(directory : str):
    path=add_trailing_slash(directory)
    if not os.path.exists(directory):
        os.makedirs(directory)

        
@logger("Old file deleted:",show_first_argument=True)
def delete_if_exists(filepath : str):
    if os.path.exists(filepath): 
        os.remove(filepath)
        
        
def get_latest_file(directory : str) -> str:
    directory = add_trailing_slash(directory)
    list_of_files = glob.glob(directory+'*')
    latest_file = max(list_of_files, key=os.path.getmtime)
    return os.path.basename(latest_file)      