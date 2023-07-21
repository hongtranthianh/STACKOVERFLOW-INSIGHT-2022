import pandas as pd
import Plot_functions as f

def rename_func(string, separator, rename_val_dict):
    '''
    Input:
        string: a string needs text inside to be renamed
        separator: separator to separate texts in the string (e.g., ';', ',')
        rename_val_dict: a dictionary indicates new text (key) and which text in the string need to rename (value)  
    Output:
        The string with texts renamed
    
    Example:
        string = 'Database administrator;Cloud infrastructure engineer'
        rename_val_dict = {'Data': ['Engineer, data','Database administrator']}
        Result: 'Data'
    '''
    new_dev_type = ''
    for i in string.split(separator):
        for j in rename_val_dict:
            for k in rename_val_dict[j]:
                if i==k and j not in new_dev_type:
                    new_dev_type = new_dev_type + j + separator
    new_dev_type = new_dev_type[:-1]
    return new_dev_type


def rename_to_df_func(df, col, separator, rename_val_dict):
    '''
    Input:
        df: dataframe to apply
        col: column contains multiple texts inside and need to be renamed
        separator: separator in the column (e.g., ';', ',')
        rename_val_dict: a dictionary indicates new text (key) and which text in the column need to rename (value)
    Output:
        A dataframe with selected column has value renamed
    '''
    df_rename = df.copy()
    for i in range(df_rename.shape[0]):
        df_rename[col].values[i] = rename_func(df_rename[col].values[i],
                                               separator,
                                               rename_val_dict)
    return df_rename


def separate_column_func (df_rename, col, separator):
    '''
    Input:
        df_rename: get from function 'rename_to_df_func'
        col: column to be separated
        separator: demiliter in the selected column
    Output: a dataframe with selected column to be seprated into multiple ones
    '''
    # Separate col into multiple ones
    df_transform = df_rename.copy()
    df_transform = df_transform[col].str.split(separator, expand=True)
    df_remaining = df_rename.loc[:,df_rename.columns!=col]
    df_transform = pd.concat([df_remaining, df_transform], axis=1)
    # Rename column
    for i in df_transform.columns[df_remaining.shape[1]:]:
        df_transform.rename(columns={i: '{0}_{1}'.format(col, i+1)}, inplace=True)
    
    return df_transform


def groupby_pivot_df_func(df_transform):
    '''
    This function is only used for anlyzing DevType and EdLevel
    Input:
        df_transform: get from function 'separate_column_func'
    Output:
        A dataframe with value count for each education level as per dev type
    '''
    df_union = pd.DataFrame(columns = ['DevType','EduLevel','Count'])

    for col in df_transform.columns[1:]:
        df_groupby = df_transform.groupby([col,'EdLevel']).size().reset_index()
        df_groupby.columns = ['DevType','EduLevel','Count']
        df_union = pd.concat([df_union, df_groupby])
    
    df_ = df_union.groupby(['DevType','EduLevel'])['Count'].sum().reset_index()
    val_count_df = pd.pivot_table(df_, index='DevType', columns='EduLevel')['Count'].reset_index()

    val_count_df = val_count_df[['DevType','Some college/university without degree','Associate degree',
                                 'Bachelor’s degree','Master’s degree','Doctoral degree','Professional degree',
                                 'Others']]
    
    return val_count_df


def analyze_dev_type(df, col, separator, rename_val_dict, bar_chart_type, chart_title, chart_xlabel, chart_ylabel, chart_x_fig, chart_y_fig):
    '''
    This function is only used for anlyzing DevType and EdLevel
    Input:
        df: a dataframe containing two columns to be analyzed (i.e., EdLevel and DevType)
        col: column (i.e., 'DevType') containing text with 'separator'
        separator: e.g., ';', ','
        rename_val_dict: a dictionary indicates new text (key) and which text in the column need to rename (value)
        bar_chart_type: either 'horizontal' or 'vertical'
        chart_title, chart_xlabel, chart_ylabel, chart_x_fig, chart_y_fig: parameters for either 'group_bar_chart' or 'group_barh_chart' function

    Output: a group bar chart showing count of education level in each job group
    '''
    
    # Replace value in DevType column
    df_rename = rename_to_df_func(df, col, separator, rename_val_dict)

    # Remove row without value in 'DevType'
    df_rename = df_rename[df_rename[col]!='']

    # Separate column 'DevType' into multiple ones
    df_transform = separate_column_func(df_rename, col, separator)

    # Group by and pivot to get value count for each education level as per dev type
    val_count_df = groupby_pivot_df_func(df_transform)

    # Group bar chart or group barh chart
    if bar_chart_type == 'vertical':
        f.group_bar_chart(val_count_df,
                          col,
                          chart_title,
                          chart_xlabel,
                          chart_ylabel,
                          x_fig = chart_x_fig,
                          y_fig = chart_y_fig)
        
    if bar_chart_type == 'horizontal':
        f.group_barh_chart(val_count_df,
                           col,
                           chart_title,
                           chart_xlabel,
                           chart_ylabel,
                           x_fig = chart_x_fig,
                           y_fig = chart_y_fig)
    

