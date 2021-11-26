import requests
from zipfile import ZipFile
# import glob
import os
import pandas as pd
# import chardet
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

def set_legend_right() -> None:
    """
    Returns:
    --------
        None
    """
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left', ncol=1)
    return

def getfile(url, path):
    r = requests.get(url, allow_redirects=True)
    open(path, 'wb').write(r.content)
    
def unzip(data_dir, file):
    with ZipFile(os.sep.join([data_dir,file]), 'r') as zipObj:
       zipObj.extractall(data_dir)
    
def xlsx2xls(directory,file, libreoffice_cmd, inplace=True):
    command = 'cd ' + directory + ' ; ' + libreoffice_cmd + ' --convert-to xls ./' + file
    os.system(command)
    if inplace:
        os.system('cd ' + directory + ' ; rm ' + file)      
        
def was_modified_today(filepath):
    modified = os.path.getmtime(filepath)
    return pd.to_datetime('today').date() == pd.to_datetime(modified, unit='s').date()


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

def logformat():
    fmt = lambda x, pos: '{:.6f}'.format(x, pos).rstrip('0').rstrip('.')
    return fmt




def plot(
    plotdf, 
    cols_to_plot, 
    xlim=None, 
    ylim=None, 
    fmt=None, 
    color=None, 
    logy=None, 
    xlabel=None, 
    ylabel=None, 
    title=None, 
    fontsize=8,
    grid=True
    ):
    """
    Custom function for data frame plotting

    Args:
    -----
        As in pandas.DataFrame.plot

    """
    
    fig, ax = plt.subplots()
    if color:
        plotdf.plot(y=cols_to_plot,ax=ax,logy=logy,grid=grid,fontsize=fontsize, color=color)
    else:
        plotdf.plot(y=cols_to_plot,ax=ax,logy=logy,grid=grid,fontsize=fontsize)
    
    ax.set_xlim( xlim )
    ax.set_ylim( ylim )

    ax.set(title=title)

    if xlabel:
        ax.set(xlabel=xlabel)
    ax.set(ylabel=ylabel)

    if fmt:
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt))

    set_legend_right()
    plt.show()
    figure = ax.figure

    return figure

def save_fig(figure, img_dir, figname, figfmt):
    figure.savefig(os.sep.join([img_dir,figname]), format = figfmt, bbox_inches='tight',facecolor='white', transparent=False) 
    return

def display_all_col(df):
    pd.set_option('display.max_columns', None)
    display(df)
    pd.reset_option('display.max_columns')
    return

def display_all_rows(df):
    pd.set_option('display.max_rows', None)
    display(df)
    pd.reset_option('display.max_rows')
    return

def display_all(df):
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    display(df)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
    return

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