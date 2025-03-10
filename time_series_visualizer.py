import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()



# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', sep=',', index_col='date', parse_dates=['date'])


# Clean data
df = df[(df['value'] < df['value'].quantile(0.975)) & (df['value'] > df['value'].quantile(0.025))]



'''Create a draw_line_plot function that uses Matplotlib to draw a line chart similar to "examples/Figure_1.png". 
The title should be Daily freeCodeCamp Forum Page Views 5/2016-12/2019. 
The label on the x axis should be Date and the label on the y axis should be Page Views.'''

def draw_line_plot():
    # Draw line plot
    fig = plt.figure(figsize=(14,7))
    plt.plot(df.index, df['value'], 'r')

    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')


    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


'''Create a draw_bar_plot function that draws a bar chart similar to "examples/Figure_2.png". 
It should show average daily page views for each month grouped by year. 
The legend should show month labels and have a title of Months. 
On the chart, the label on the x axis should be Years and the label on the y axis should be Average Page Views.'''

'''df_bar = df.groupby([df.index.year, df.index.month])['value'].mean()
print(df_bar)'''

def draw_bar_plot():
    
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()

    ''' Need to define columns to group data by. Index already parsed as date earlier.'''
    df_bar["Year"]= df_bar.index.year
    df_bar["Month"] = df_bar.index.month

    '''Map name of months over numerical value of months for use in Legend'''
    Month_labels = {1: "January",
     2: "Feburary",
     3:"March",
     4: "April",
     5: "May",
     6: "June",
     7: "July",
     8: "August",
     9: "September",
     10: "October",
     11: "November",
     12: "December"}
    df_bar['Month'] = df_bar['Month'].map(Month_labels)

    '''Grouping the values by year and month and taking the mean.'''
    df_bar = df_bar.groupby(['Year', 'Month'])['value'].mean().reset_index()

    # Draw bar plot
    fig = plt.figure(figsize=(12,6))
    '''Need to manually set hue_order so that January is assigned the first value of the legend rather then the position it appears in the data set
    which would be in 2017 and so after half the other months.'''
    Month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    '''Paired colour palette chosen as it has 12 distinct colours. '''

    ''' Had an error when plotting barplot
    "AttributeError: module 'numpy' has no attribute 'float'.

    `np.float` was a deprecated alias for the builtin `float`. 
    To avoid this error in existing code, use `float` by itself. Doing this will not modify any behavior and is safe. 
    If you specifically wanted the numpy scalar type, use `np.float64` here."

    the following two lines fixed
    '''
    import numpy as np
    np.float = float
    sns.barplot(data=df_bar, x = 'Year', y='value', hue = 'Month', hue_order = Month_order, palette = "Paired")

    plt.xlabel("Years")
    plt.ylabel("Average Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


'''
Create a draw_box_plot function that uses Seaborn to draw two adjacent box plots similar to "examples/Figure_3.png". 
These box plots should show how the values are distributed within a given year or month and how it compares over time. 
The title of the first chart should be Year-wise Box Plot (Trend) and the title of the second chart should be Month-wise Box Plot (Seasonality). 
Make sure the month labels on bottom start at Jan and the x and y axis are labeled correctly. 
The boilerplate includes commands to prepare the data.
'''

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)

    ''' Need January to come first, assign a numeric month column as I did for the barchart task
    Then sort data by numeric values 1-12'''
    df_box["month numeric"] = df_box.date.dt.month
    df_box = df_box.sort_values("month numeric")

    ''' Plot two boxplots using subplot'''
    fig, axs = plt.subplots(1, 2, figsize=(18,10)) 
    axs[0] = sns.boxplot(data = df_box, x = 'year', y = 'value', ax=axs[0])
    axs[1] = sns.boxplot(data = df_box, x = 'month', y = 'value', ax=axs[1])

    axs[0].set_title('Year-wise Box Plot (Trend)')
    axs[0].set_xlabel('Year')
    axs[0].set_ylabel('Page Views')

    axs[1].set_title('Month-wise Box Plot (Seasonality)')
    axs[1].set_xlabel('Month')
    axs[1].set_ylabel('Page Views')


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
