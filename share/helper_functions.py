import requests
from zipfile import ZipFile
# import glob
import os
import glob
import pandas as pd
# import chardet
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from sorcery import dict_of, unpack_keys

# --------------------------------------------------------------------------    

def split_dict_by_keys(base_dict : dict, split_keys : list) -> dict:
        """
        Split dict by keys given in split_keys list

        Args:
            base_dict: dict
                Base dictionary to split. It will not be modified.

            split_keys: list
                Base list of keys according to which the dict will be split.
                The list will not be modified.

        Returns:
            (dict, dict)
                Dict of items found in split_keys list, dict of items NOT found in split_keys list
        """
        dict_not_in_split_keys_list = base_dict.copy()
        clear_split_keys = split_keys.copy()
        for d in split_keys:
            if not dict_not_in_split_keys_list.get(d):
                clear_split_keys.remove(d)

        # https://stackoverflow.com/questions/41330311/split-dictionary-depending-on-key-lists
        dict_in_split_keys_list = dict((d, dict_not_in_split_keys_list.pop(d)) for d in clear_split_keys)
        return dict_in_split_keys_list, dict_not_in_split_keys_list

# --------------------------------------------------------------------------    
def ls(pattern : str):
    """
    Lists files and directories in the current working directory.

    Args:
    -----
        pattern : str
            ls('*') lists all.

    Returns:
    --------
        list of str
            List of file and directory names
    """
    return glob.glob(pattern)
# -------------------------------------------------------------------------------

def set_legend_right(oldparams):
    """
    Generate legend params to set the legend on the right, outside of the plot

    Args:
    -----
        oldparams : dictionary
    
    Returns
    -------
        newparams : dictionary
            oldparams + params for setting the legend on the right, outside of the plot
    """
    params = dict_of(bbox_to_anchor=(1, 1), loc='upper left', ncol=1)
    newparams = {**oldparams, **params}
    return newparams
# -------------------------------------------------------------------------------

def getfile(url : str, savepath : str) -> None:
    """
    Get file from URL

    Args:
    -----
        url : str

        savepath : str

    Returns:
    --------
        None
    """
    r = requests.get(url, allow_redirects=True)
    open(savepath, 'wb').write(r.content)
    return

# -------------------------------------------------------------------------------

def unzip(data_dir : str, file : str) -> None:
    """
    Args:
    -----
        data_dir  : str
            
        file : str
            
    Returns:
        None
 
    """
    
    with ZipFile(os.sep.join([data_dir,file]), 'r') as zipObj:
       zipObj.extractall(data_dir)
    return
# -------------------------------------------------------------------------------
    
def xlsx2xls(directory : str,file : str, libreoffice_cmd : str, inplace : bool =True) -> None:
    """
    Args:
    -----
        directory : str

        file : str

        libreoffice_cmd : str

        inplace : bool=True

    Returns:
    --------
        None
    """
    command = 'cd ' + directory + ' ; ' + libreoffice_cmd + ' --convert-to xls ./' + file
    os.system(command)
    if inplace:
        os.system('cd ' + directory + ' ; rm ' + file)
    return    
# -------------------------------------------------------------------------------
        
def was_modified_today(filepath : str) -> bool:
    """
    Args:
    -----
        filepath : str

    Returns:
    --------
        bool
    """
    modified = os.path.getmtime(filepath)
    return pd.to_datetime('today').date() == pd.to_datetime(modified, unit='s').date()

# -------------------------------------------------------------------------------

def download_if_not_modified_today(path : str, download_command : str) -> None:
    """
    Args:
        path : str
        download_command : str

    Returns:
        None
    """
    
    if os.path.exists(path):
        print(path + ' exists')
        if was_modified_today(path):
            print(path + ' was modified today, not downloading')
        else:
            print(path + ' was not modified today')
            print('Downloading...')
            os.system(download_command)
            print(path + ' downloaded')
    else:
        print(path + ' does not exist')
        print('Downloading...')
        os.system(download_command)
        print(path + ' downloaded')
    return


# -------------------------------------------------------------------------------

# def csvs2df(data_dir):
#     # merges all csv files in directory into one data frame
#     all_files = sorted(glob.glob(os.path.join(data_dir, "*.csv")) ,key=str.lower)
#     dfs = []
#     for f in all_files: 
#         raw_data = open(f, 'rb').read()
#         encoding=chardet.detect(raw_data)['encoding']
#         if encoding == 'Windows-1252':
#             encoding = 'Windows-1250'  
#         dfs.append(pd.read_csv(f,encoding = encoding,sep=';'))
#     concatenated_df   = pd.concat(dfs, ignore_index=True)
#     return concatenated_df

# -------------------------------------------------------------------------------

def logformat() -> str:
    """
    Generate format string for clean notation in log scale: 0.01, 0.1, 1, 10, 100 (strip unnecessary zeros)

    Returns:
    --------
        str
            Format string
    """
    fmt = lambda x, pos: '{:.6f}'.format(x, pos).rstrip('0').rstrip('.')
    return fmt

# -------------------------------------------------------------------------------



def plot(
    plotdf, 
    y = None, 
    xlim=None, 
    ylim=None, 
    fmt=None, 
    color=None, 
    logy=None, 
    xlabel=None, 
    ylabel=None, 
    title=None, 
    fontsize=8,
    grid=True,
    legendlabels=None,
    legendtitle = None
    ):
    """
    Custom function for data frame plotting

    Args:
    -----
        plotdf : pandas.DataFrame

        y
            Data frame columns

        xlim, 
        ylim, 
        fmt, 
        color, 
        logy, 
        xlabel, 
        ylabel, 
        title, 
        fontsize,
        grid
            As in pandas.DataFrame.plot

        legendlabels : list
            Legend labels for pyplot

        legendtitle : str
            Legend title for pyplot
        
        Returns:
        --------
        matplotlib.figure.Figure
    """
    
    
    fig, ax = plt.subplots()
    
    dfplotoptions = {}

    if color:
        dfplotoptions['color'] = color
    if y:
        dfplotoptions['y'] = y
    plotdf.plot(ax=ax,logy=logy,grid=grid,fontsize=fontsize, **dfplotoptions) # Perhaps more options can be put to dict
    
    
    ax.set_xlim( xlim )
    ax.set_ylim( ylim )

    ax.set(title=title)

    if xlabel:
        ax.set(xlabel=xlabel)
    ax.set(ylabel=ylabel)

    if fmt:
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt))

    legendparams = {}
    if legendlabels:
        dict = dict_of(labels=legendlabels)
        legendparams = {**legendparams, **dict}

    if legendtitle:
        dict = dict_of(title = legendtitle)
        legendparams = {**legendparams, **dict}
    
    legendparams = set_legend_right(legendparams)
    ax.legend(**legendparams)
    plt.show()
    figure = ax.figure

    return figure
# -------------------------------------------------------------------------------

def save_fig(figure, img_dir, figname, figfmt) -> None:
    """
    Args:
    -----
        figure
        
        img_dir
        
        figname
        
        figfmt

    Returns:
    --------
        None
    """
    figure.savefig(os.sep.join([img_dir,figname]), format = figfmt, bbox_inches='tight',facecolor='white', transparent=False) 
    return
# -------------------------------------------------------------------------------

def display_all_col(df) -> None:
    """
    Args:
    -----
        df
            pandas data frame

    Returns:
    --------
        None
    """
    pd.set_option('display.max_columns', None)
    display(df)
    pd.reset_option('display.max_columns')
    return
# -------------------------------------------------------------------------------

def display_all_rows(df) -> None:
    """
    Args:
    -----
        df
            pandas data frame

    Returns:
    --------
        None
    """
    pd.set_option('display.max_rows', None)
    display(df)
    pd.reset_option('display.max_rows')
    return
# -------------------------------------------------------------------------------

def display_all(df) -> None:
    """
    Args:
    -----
        df
            pandas data frame

    Returns:
    --------
        None
    """
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    display(df)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
    return
# -------------------------------------------------------------------------------

# ################### Dostosować:

# # https://stackoverflow.com/a/43157792
# class PlotOptions(NamedTuple):
#     xlabel: str = None
#     ylabel: str = None
#     title: str=None
#     legend: str=None
#     cmap: mpl.colors.LinearSegmentedColormap = mpl.cm.Blues
#     ylim: tuple=None
        
# def matplotlib_plot(df, dftrend = None):
#     fig, ax = plt.subplots()
#     df.plot(ax=ax)
#     if exists_df(dftrend):
#         dftrend['Trend 2020'].plot(ax=ax)
#         dftrend['Trend 2021'].plot(ax=ax)
#     return fig, ax



# def set_matplotlib_plot_options(fig, ax, plot_options, dftrend=None):
#     set_ticks(rotation=0)
#     set_minor_ticks(ax)
#     set_grid(ax)
#     set_axes_labels(ax,plot_options)
#     set_colors(ax, plot_options)
#     set_last_line_thicker(ax, dftrend) # przenieść dftrend do plotoptions
#     set_last_line_color(ax, dftrend)
#     set_legend(plot_options)
#     set_title(ax,plot_options)
#     return

# def plot_df(df, plot_options, dftrend=None):
#     fig, ax = matplotlib_plot(df, dftrend)
#     if plot_options.ylim: 
# #         print(plot_options.ylim)
#         ax.set_ylim(plot_options.ylim)
#     set_matplotlib_plot_options(fig, ax, plot_options, dftrend)
#     plt.show()
#     ylim = ax.get_ylim()
#     return fig, ylim

# def set_legend(plot_options):
#     if plot_options.legend:
#         plt.legend(plot_options.legend, loc='center left', bbox_to_anchor=(1.0, 0.5))
#     else:
#         plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
#     return

# def set_ticks(rotation):
#     plt.xticks(rotation=rotation)
#     return

# def set_grid(ax):
#     ax.xaxis.grid()
#     ax.yaxis.grid()
#     return

# # Dać to do plot_options
# def set_last_line_thicker(ax, dftrend):
#     if exists_df(dftrend):
#         ax.lines[-4].set_linewidth(4)
#         ax.lines[-3].set_linewidth(4)
#         ax.lines[-2].set_linewidth(4)
#         ax.lines[-1].set_linewidth(4)
#     else:    
#         ax.lines[-2].set_linewidth(4)
#         ax.lines[-1].set_linewidth(4)
#     return

# # Dać to do plot_options
# def set_last_line_color(ax, dftrend=None):
#     if exists_df(dftrend):
#         ax.lines[-4].set_color('Red')
#         ax.lines[-3].set_color('limegreen')
#         ax.lines[-2].set_color('darkred')
#         ax.lines[-1].set_color('green')
#     else:
#         ax.lines[-2].set_color('Red')
#         ax.lines[-1].set_color('limegreen')  
#     return

# # https://matplotlib.org/3.3.3/gallery/ticks_and_spines/tick-locators.html
# def set_minor_ticks(ax):
#     ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
#     return

# def set_axes_labels(ax,plot_options):
#     if plot_options.xlabel:
#         ax.set(xlabel=plot_options.xlabel)
#     if plot_options.ylabel:
#         ax.set(ylabel=plot_options.ylabel)
#     return

# def set_title(ax,plot_options):
#     if plot_options.title:
#         ax.set(title=plot_options.title)

# def make_color_map(cmap, vmin, vmax):
#     norm = mpl.colors.Normalize(vmin, vmax)
#     cmap = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
#     cmap.set_array([])
#     return cmap

# # https://stackoverflow.com/questions/52758070/color-map-to-shades-of-blue-python/52758206
# def set_colors(ax, plot_options):
#     offset = 2
#     norm_min = 0
#     norm_max = len(ax.lines)+2*offset
#     cmap = make_color_map(cmap=plot_options.cmap, vmin=norm_min, vmax=norm_max)
#     for i in range(0,len(ax.lines)):
#         ax.lines[i].set_color(cmap.to_rgba( i+offset))
#     return