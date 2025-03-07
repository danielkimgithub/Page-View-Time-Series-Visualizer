import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True)
#df['date'] = pd.to_datetime(df['date'])
#df = df.set_index('date')

# Clean data 
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots()
    ax.set(title = "Daily freeCodeCamp Forum Page Views 5/2016-12/2019",
           xlabel = "Date",
           ylabel = "Page Views"
           )
    sns.lineplot(data=df, legend=False, palette=['r'])

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar["Years"] = df_bar.index.year
    df_bar["Month"] = df_bar.index.month

    df_bar = df_bar.groupby(["Years", "Month"], sort=False)["value"].mean()
    df_bar = df_bar.unstack()
    df_bar.columns = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    # Draw bar plot
    fig = df_bar.plot(
        kind = 'bar', figsize=(15, 10)).figure
    plt.xlabel('Years', fontsize=15)
    plt.ylabel('Average Page Views', fontsize=15)
    plt.legend(loc='upper left', title = 'Month', fontsize=15)
    plt.xticks(rotation=90)

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1,2)
    sns.boxplot(data = df_box, x = 'year', y='value', ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')  

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(data = df_box, x='month', y='value', order = months, ax=axes[1]) 
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')  

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
