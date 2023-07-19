import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style

def histogram(df, col, bin, title, xlabel, ylabel, color='#c38e1a', edgecolor='#f0d195', x_fig=6, y_fig=4):
    '''
    Input:
      df: dataframe to use
      col: column to use for histogram
      bin: number of bins to group data into "bins" of equal width
      title: title of the chart
      xlabel: label of x axis
      ylabel: label of y axis
      color: color of bar
      x_fig: width of figure
      y_fig: height of figure
    Output: histogram
    '''
    # Remove missing value
    df_col = df[[col]][~df[col].isnull()]
    # Histogram
    plt.style.use('ggplot')
    df_col.hist(bins=bin, figsize=(x_fig, y_fig), color=color, edgecolor=edgecolor)
    plt.title(title, y=1.05)
    plt.xlabel(xlabel, fontsize = 10, labelpad=10, weight='bold')
    plt.ylabel(ylabel, fontsize = 10, labelpad=10, weight='bold')
    # Format y-axis label with thousand comma separator
    y_axis_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(['{:,.0f}'.format(i) for i in y_axis_values])
    # Add respondent total to top right of the chart
    total_respondent = df_col.shape[0]
    x_text = df_col.max()-20
    y_text = df_col.value_counts().max()
    plt.text(x_text, y_text,'Total respondents: {0}'.format('{:,.0f}'.format(total_respondent)),
             fontsize = 8.5,
             bbox = dict(facecolor = '#ffffff', edgecolor = '#2c2b2b', boxstyle = 'round,pad=.6'));


def bar_chart(df, col, title, xlabel, ylabel, x_order, bar_color='#c38e1a', x_fig=6, y_fig=4):
    '''
    Input:
      df: dataframe to use
      col: column to use for bar chart
      title: title of the chart
      xlabel: label of x axis
      ylabel: label of y axis
      x_order: specify value order to sort category label of x axis
      bar_color: color of bar chart
      x_fig: width of figure
      y_fig: height of figure
    Output: vertical bar chart
    '''
    plt.style.use('ggplot')
    # Bar chart
    plot = df[col].value_counts()\
                  .reindex(x_order)\
                  .plot(kind='bar', figsize=(x_fig, y_fig), rot=0, color = bar_color)
    # Add data labels
    for p in plot.patches:
      plot.annotate(
          str('{:,.0f}'.format(p.get_height())), # format with thousand comma separator
          xy=(p.get_x() + 0.25, p.get_height() + 300),
          fontsize=9,
          ha='center')
    #Add title, x-axis and y-axis label
    plt.title(title, y=1.05)                                        
    plt.xlabel(xlabel, fontsize = 10, labelpad=10, weight='bold')
    plt.ylabel(ylabel, fontsize = 10, labelpad=10, weight='bold')
    # Format y-axis label with thousand comma separator
    y_axis_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(['{:,.0f}'.format(i) for i in y_axis_values])


def percent_bar_chart(df, col, total_respondent, title, xlabel, ylabel, x_order, bar_color='#c38e1a', x_fig=6, y_fig=4):
    '''
    Input:
      df: dataframe to use
      col: column to use for bar chart
      total_respondent: number of total respondents
      title: title of the chart
      xlabel: label of x axis
      ylabel: label of y axis
      x_order: specify value order to sort category label of x axis
      bar_color: color of bar chart
      x_fig: width of figure
      y_fig: height of figure
    Output: vertical bar chart with percent number
    '''
    # Transform df for plot
    val_count_df = df[col].value_counts().apply(lambda x: x*100/total_respondent)
    # Bar chart
    plt.style.use('ggplot')
    plot = val_count_df.reindex(x_order)\
                       .plot(kind='bar', figsize=(x_fig, y_fig), rot=0, color = bar_color)
    # Add respondent total to top right of the chart
    plt.text(x_fig/1.5, val_count_df.max()-1,
             'Total respondents: {0}'.format('{:,.0f}'.format(total_respondent)),
             fontsize = 8.5,
             bbox = dict(facecolor = '#ffffff', edgecolor = '#2c2b2b', boxstyle = 'round,pad=.6'))
    # Add data labels
    for p in plot.patches:
      plot.annotate(
          str(round(p.get_height(), 2)) + '%',
          xy=(p.get_x() + 0.25, p.get_height() + 1),
          fontsize=9,
          ha='center')
    # Add title, x-axis and y-axis label
    plt.title(title, y=1.05)                                        
    plt.xlabel(xlabel, fontsize = 10, labelpad=10, weight='bold')
    plt.ylabel(ylabel, fontsize = 10, labelpad=10, weight='bold')


def value_count_func(df, col, separator):
    '''
    Input:
        df: dataframe
        col: a column contains multiple answers (or types) and separated by semicolon, or colon, etc
    Output: A dataframe contains value count for each type
    '''
    ## Create a new dataframe only containing the selected column
    col_df = df[[col]]
    ## Separate the column into multiple ones
    col_df = col_df[col].str.split(separator, expand=True)
    ## Rename the columns
    for i in range(col_df.shape[1]):
        col_df.rename(columns = {i:'Type_{0}'.format(i+1)}, inplace=True)
    ## Get value count for each type
    ### Create an empty dataframe
    df_union = pd.DataFrame(columns=['Type','Count'])
    ### Iterate over each method column 
    for i in col_df:
        col_df_ = col_df[i].value_counts().reset_index()
        col_df_.columns = ['Type','Count']
        df_union = pd.concat([df_union,col_df_])
    ### Group by to get final stats
    val_count_df = df_union.groupby('Type').sum()\
                           .reset_index()\
                           .sort_values('Count', ascending=True)
    return val_count_df


def barh_chart(val_count_df, title, xlabel, bar_color='#c38e1a', x_fig=5, y_fig=7):
    '''
    Input:
      val_count_df: a dataframe contains value count of each row
      title: title of the chart
      xlabel: label of x axis
      bar_color: color of bar chart
      x_fig: width of figure
      y_fig: height of figure
    Output: horizontal bar chart
    '''
    plt.style.use('ggplot')
    plt.figure(figsize=(x_fig,y_fig))
    plt.barh(val_count_df.iloc[:,0], val_count_df.iloc[:,1], color=bar_color)
    plt.title(title, y=1.05)
    plt.xlabel(xlabel, fontsize = 10, labelpad=10, weight='bold')
    # Add data value and format with thousand comma separator
    for index, value in enumerate(val_count_df.iloc[:,1]):
        plt.text(value+4200, index-.1, str('{:,.0f}'.format(value)), ha='center', fontsize=9)
    # Format x-axis label with thousand comma separator
    x_axis_values = plt.gca().get_xticks()
    plt.gca().set_xticklabels(['{:,.0f}'.format(i) for i in x_axis_values])


def percent_barh_chart(val_count_df, total_respondent, title, xlabel, bar_color='#c38e1a', x_fig=5, y_fig=7):
    '''
    Input:
      val_count_df: a dataframe contains value count of each row
      total_respondent: number of total respondents
      title: title of the chart
      xlabel: label of x axis
      bar_color: color of bar chart
      x_fig: width of figure
      y_fig: height of figure
    Output: horizontal bar chart
    '''
    # Transform df for plot
    percent_val_count_df = val_count_df
    percent_val_count_df.iloc[:,1] = percent_val_count_df.iloc[:,1].apply(lambda x: x*100/total_respondent)
    # Horizontal bar chart
    plt.style.use('ggplot')
    plt.figure(figsize=(x_fig,y_fig))
    plt.barh(percent_val_count_df.iloc[:,0], percent_val_count_df.iloc[:,1], color=bar_color)
    plt.title(title, y=1.05)
    plt.xlabel(xlabel, fontsize = 10, labelpad=10, weight='bold')
    # Add data value and format with thousand comma separator
    for index, value in enumerate(percent_val_count_df.iloc[:,1]):
        plt.text(value+2, index-.1, str(round(value, 2)) + '%', ha='center', fontsize=9)
    # Add respondent total to bottom right of the chart
    plt.text(percent_val_count_df.iloc[:,1].max()/2, y_fig - 7.2,
             'Total respondents: {0}'.format('{:,.0f}'.format(total_respondent)),
             fontsize = 8.5,
             bbox = dict(facecolor = '#ffffff', edgecolor = '#2c2b2b', boxstyle = 'round,pad=.6'))
        

def group_bar_chart(val_count_df, common_col, title, xlabel, ylabel, bar_color='#c38e1a', x_fig=5, y_fig=7):
    '''
    Input:
      val_count_df: a dataframe contains value counts for each column per group whose value is in common_col
      common_col: common column to show in x_axis
      title: title of the chart
      xlabel: label of x axis
      ylabel: label of y axis
      bar_color: color of bar chart
      x_fig: width of figure
      y_fig: height of figure
    Output: vertical group bar chart
    '''
    # Transform df for plot
    val_count_df = val_count_df.set_index(common_col)
    # Group bar chart
    plt.style.use('ggplot')
    val_count_df.plot(kind='bar',\
                      rot = 0,\
                      # color={val_count_df.columns[0]: '#c38e1a', val_count_df.columns[1]:'#dec25b'},\
                      figsize=(x_fig, y_fig))
    plt.title(title, y=1.05)
    plt.xlabel(xlabel, fontsize = 10, labelpad=10, weight='bold')
    plt.ylabel(ylabel, fontsize = 10, labelpad=10, weight='bold')
    ## Format y-axis label with thousand comma separator
    y_axis_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(['{:,.0f}'.format(i) for i in y_axis_values])


def group_barh_chart(val_count_df, common_col, title, xlabel, ylabel, bar_color='#c38e1a', x_fig=5, y_fig=7):
    '''
    Input:
      val_count_df: a dataframe contains value counts for each column per group whose value is in common_col
      common_col: common column to show in x_axis
      title: title of the chart
      xlabel: label of x axis
      ylabel: label of y axis
      bar_color: color of bar chart
      x_fig: width of figure
      y_fig: height of figure
    Output: horizontal group bar chart
    '''
    # Transform df for plot
    val_count_df = val_count_df.set_index(common_col)
    # Group bar chart
    plt.style.use('ggplot')
    val_count_df.plot(kind='barh',\
                      rot = 0,\
                      # color={val_count_df.columns[0]: '#c38e1a', val_count_df.columns[1]:'#dec25b'},\
                      figsize=(x_fig, y_fig))
    plt.title(title, y=1.05)
    plt.xlabel(xlabel, fontsize = 10, labelpad=10, weight='bold')
    plt.ylabel(ylabel, fontsize = 10, labelpad=10, weight='bold')
    ## Format x-axis label with thousand comma separator
    x_axis_values = plt.gca().get_xticks()
    plt.gca().set_xticklabels(['{:,.0f}'.format(i) for i in x_axis_values])    