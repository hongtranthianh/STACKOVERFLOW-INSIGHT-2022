import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import Wrangling_functions as f1
import Plot_functions as f2


def to_list_of_list_func(list):
    '''
    Input:
        list = ['a', 'b', 'c']
    Output:
        list = [['a'],['b'],['c']]
    '''
    return [[i] for i in list]


def df_for_graph_func(df, col_list, separator, top_n):
    '''

    '''
    # Filter df with selected columns
    df = df[col_list]
    # Get a list of lists of top n in terms of popular technology
    topn_list = []
    for col in col_list:
        k = f2.value_count_func(df,col,separator).sort_values(by='Count',ascending=False)['Type'].to_list()[:top_n]
        topn_list.append(k)
        
    # Get a list of dictionaries of top n in terms of popular technology
    rename_dict = []
    for i,col in enumerate(col_list):
        element = dict(zip(topn_list[i], to_list_of_list_func(topn_list[i])))
        rename_dict.append(element)

    # Fill NA for the df to avoid error when applying function "f1.rename_to_df_func"
    NoNull_df = df.fillna('')

    # Only keep values that belong to top n of popular technology
    rename_df = NoNull_df
    for i,col in enumerate(col_list):
        rename_df = f1.rename_to_df_func(rename_df, col, separator, rename_dict[i])

    # Separate into multiple columns
    sep_df = rename_df.copy()
    for col in rename_df.columns:
        sep_df = f1.separate_column_func(sep_df, col, separator)

    # Convert None to empty string
    graph_df = sep_df.fillna('')

    return rename_df, graph_df


def get_node_size_dict_func(df, col, separator):
    '''

    '''
    val_count_df = f2.value_count_func(df, col, separator)
    percent_val_count_df = val_count_df[val_count_df.iloc[:,0]!='']
    percent_val_count_df.iloc[:,1] = percent_val_count_df.iloc[:,1].apply(lambda x: x*100/percent_val_count_df.iloc[:,1].sum())
    col_node_size = {k : v for k,v in percent_val_count_df.values}

    return col_node_size


def networkx_graph(graph_df, rename_df, title, x_fig=9, y_fig=6, edge_color='#d6d5d5'):
    '''

    '''
    # Get list of column name in graph_df
    columns = list(graph_df.columns.values)

    # Create an empty graph
    g = nx.empty_graph(0, nx.DiGraph())
    fig = plt.figure(figsize=(x_fig, y_fig))

    # Create edge between 2 values, between all consecutive coumns
    for i in range(len(columns)-1):
        g.add_edges_from(zip(graph_df[columns[i]], graph_df[columns[i+1]]), weight=3)

    # Set spring layout for the graph
    pos = nx.spring_layout(g)
    
    # Remove None node, otherwise it raises an error
    g.remove_node('')

    # Get a list of dictionaries of node size
    node_size_dict = []
    for col in rename_df.columns:
        element = get_node_size_dict_func(rename_df,col,';')
        node_size_dict.append(element)
    # Get a dictionary of node size
    all_dict = node_size_dict[1:]
    node_size_ = node_size_dict[0]
    for i in all_dict:
        node_size_ = {k:v for d in (node_size_,i) for k,v in d.items()}
        
    # Set node color
    color = ['#58bf1e','#f0ef5d','#f5b849','#f86132','#3cdcbc','#5fcef9']
    c = []
    for node in g.nodes(data=True):
        for i, value in enumerate(node_size_dict):
            if node[0] in value.keys():
                c.append(color[i])

    # Plot network graph
    nx.draw(g,
            pos = pos,
            with_labels = False, # remove label, add it by matplotlib instead
            # node_size = [i*50 for i in node_size_.values()],
            node_size = [node_size_[i]*50 for i in g.nodes],
            node_color = c,
            edge_color = edge_color,
            arrows = False # remove arrowhead for edges
            )
        
    # Add node label with font size based on node size
    for node, (x, y) in pos.items():
        if node != '':
            plt.text(x, y, node, fontsize = 7, ha='center', va='center')
        
    # Add legend by creating a dummy scatter plot and use its legend
    t = [col.split('_')[0] for col in columns]
    legend = list(dict([(i, 1) for i in t]).keys())
    group = []
    for node in g.nodes(data=True):
        for i, value in enumerate(node_size_dict):
            if node[0] in value.keys():
                group.append(legend[i])
    for v in set(group):
        plt.scatter([], [], c = color[legend.index(v)], label = '{}'.format(v))
    plt.legend()

    # Add title for graph
    plt.title(title,weight='bold')

    # Add total respondents
    total_respondent = graph_df.shape[0]
    plt.text(0, 0,
            'Total respondents: {0}'.format('{:,.0f}'.format(total_respondent)),
            fontsize = 8.5,
            bbox = dict(facecolor = '#ffffff', edgecolor = '#2c2b2b', boxstyle = 'round,pad=.6')
            );

    plt.show()


def get_networkx_graph(df, col_list, separator, top_n, title, x_fig=9, y_fig=6, edge_color='#d6d5d5'):
    '''

    '''
    rename_df = df_for_graph_func(df, col_list, separator, top_n)[0]
    graph_df = df_for_graph_func(df, col_list, separator, top_n)[1]
    networkx_graph(graph_df, rename_df, title, x_fig, y_fig, edge_color)

