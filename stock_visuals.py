import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec
import matplotlib.ticker as mticker
from mplfinance.original_flavor import candlestick_ohlc
import datetime
import math


fig = plt.figure()
fig.patch.set_facecolor('#6C3483')
gs = fig.add_gridspec(6,6)
ax1 = fig.add_subplot(gs[0:4, 0:4])
ax2 = fig.add_subplot(gs[0, 4:6])
ax3 = fig.add_subplot(gs[1, 4:6])
ax4 = fig.add_subplot(gs[2, 4:6])
ax5 = fig.add_subplot(gs[3, 4:6])
ax6 = fig.add_subplot(gs[4, 4:6])
ax7 = fig.add_subplot(gs[5, 4:6])
ax8 = fig.add_subplot(gs[4, 0:4])
ax9 = fig.add_subplot(gs[5, 0:4])

stock = ['BRK-B', 'AMD', 'TSLA', 'MARA', 'NIO', 'AAPL', 'AMZN']

def figure_design(ax):
    ax.set_facecolor('#2ECC71')
    ax.tick_params(axis='both', labelsize=14, colors='white')
    ax.ticklabel_format(useOffset=False)
    ax.spines['bottom'].set_color('#2C3E50')
    ax.spines['top'].set_color('#2C3E50')
    ax.spines['left'].set_color('#2C3E50')
    ax.spines['right'].set_color('#2C3E50')

def string_to_num(df, column):
    if isinstance(df.iloc[0, df.columns.get_loc(column)], str):
        df[column] = df[column].str.replace(',','')
        df[column] = df[column].astype(float)
    return df

price, change, pct_change, volume, latest_pattern, one_year_target

def read_data_ohlc(filename, stock_code, usecols):
    df = pd.read_csv(filename, header=None, usecols=usecols,
                    names=['time', stock_code, 'change', 'pct_change', 'volume', 'latest_pattern', 'one_year_target'],
                    index_col = 'time', parse_dates=['time'])

