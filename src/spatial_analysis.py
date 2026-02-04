"""
Spatial network analysis for grocery store accessibility patterns
"""

import pandas as pd
import networkx as nx
import geopandas as gpd


def build_adjacency_graph(shapefile_path='tl_2018_us_county.shp'):
    """
    Build county adjacency network from shapefile.
    """
    gdf = gpd.read_file(shapefile_path)
    
    gdf['STATE'] = gdf['STATEFP'].astype(int)
    gdf['COUNTY'] = gdf['COUNTYFP'].astype(int)
    gdf = gdf[['STATE', 'COUNTY', 'geometry']]
    
    adjacency_list = []
    
    for idx, county in gdf.iterrows():
        touching_counties = gdf[gdf.geometry.touches(county.geometry)]
        
        for _, neighbor in touching_counties.iterrows():
            adjacency_list.append({
                'County_STATE': county['STATE'],
                'COUNTY': county['COUNTY'],
                'Neighbor_STATE': neighbor['STATE'],
                'Neighbor_COUNTY': neighbor['COUNTY']
            })
    
    adjacency_df = pd.DataFrame(adjacency_list)
    adjacency_df = adjacency_df.drop_duplicates()
    adjacency_df = adjacency_df.sort_values(
        ['County_STATE', 'COUNTY', 'Neighbor_STATE', 'Neighbor_COUNTY']
    )
    
    G = nx.Graph()
    
    for _, row in adjacency_df.iterrows():
        county = (row['County_STATE'], row['COUNTY'])
        neighbor = (row['Neighbor_STATE'], row['Neighbor_COUNTY'])
        G.add_edge(county, neighbor)
    
    return adjacency_df, G


def prepare_weighted_network_data(adjacency_df, data, year, metric_col):
    """
    Merge adjacency data with economic metrics for network weighting
    """
    metric_data = data[data['YEAR'] == year].groupby(
        ['STATE', 'COUNTY', 'YEAR']
    )[metric_col].mean().reset_index()
    
    merged = adjacency_df.merge(
        metric_data,
        left_on=['County_STATE', 'COUNTY'],
        right_on=['STATE', 'COUNTY'],
        how='left'
    )
    
    merged.rename(columns={metric_col: f'{metric_col}_County'}, inplace=True)
    merged.drop(columns=['STATE'], inplace=True)
    
    final = merged.merge(
        metric_data,
        left_on=['Neighbor_STATE', 'Neighbor_COUNTY'],
        right_on=['STATE', 'COUNTY'],
        how='left',
        suffixes=('', '_Neighbor')
    )
    
    final.rename(columns={metric_col: f'{metric_col}_Neighbor'}, inplace=True)
    final.drop(columns=['STATE'], inplace=True)
    
    result = final[[
        'YEAR', 'County_STATE', 'COUNTY', f'{metric_col}_County',
        'Neighbor_STATE', 'Neighbor_COUNTY', f'{metric_col}_Neighbor'
    ]].dropna()
    
    return result


def calculate_pagerank(network_data, metric_col):
    """
    Calculate PageRank scores for counties based on weighted adjacency
    """
    G = nx.DiGraph()
    
    for _, row in network_data.iterrows():
        source = (row['County_STATE'], row['COUNTY'])
        target = (row['Neighbor_STATE'], row['Neighbor_COUNTY'])
        weight = row[f'{metric_col}_Neighbor']
        
        G.add_edge(source, target, weight=weight)
        
        if not G.has_edge(source, source):
            self_weight = row[f'{metric_col}_County']
            G.add_edge(source, source, weight=self_weight)
    
    pagerank_scores = nx.pagerank(G, weight='weight')
    
    pagerank_df = pd.DataFrame.from_dict(
        pagerank_scores, orient='index', columns=['PageRank']
    ).reset_index()
    
    pagerank_df.columns = ['County', 'PageRank']
    pagerank_df[['County_STATE', 'COUNTY']] = pd.DataFrame(
        pagerank_df['County'].tolist(), index=pagerank_df.index
    )
    pagerank_df.drop(columns=['County'], inplace=True)
    
    pagerank_df = pagerank_df.sort_values(by='PageRank', ascending=False)
    
    max_county = pagerank_df.iloc[0]
    
    return pagerank_df, (max_county['County_STATE'], max_county['COUNTY'], max_county['PageRank'])


def get_degree_centrality(adjacency_graph):
    """
    Calculate degree centrality for all counties
    """
    degrees = dict(adjacency_graph.degree)
    
    degree_df = pd.DataFrame(
        list(degrees.items()), 
        columns=["County", "Degree"]
    )
    
    degree_df[['STATE', 'COUNTY']] = pd.DataFrame(
        degree_df['County'].tolist(), index=degree_df.index
    )
    degree_df.drop(columns=['County'], inplace=True)
    
    return degree_df.sort_values(by='Degree', ascending=False)
