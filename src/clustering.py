"""
Clustering and similarity analysis for county segmentation

"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt


def calculate_county_similarity(flattened_features):
    """
    Calculate pairwise cosine similarity between counties
    """
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(flattened_features)
    
    similarity = cosine_similarity(scaled_features)
    
    state_county_geoids = flattened_features.index.map(
        lambda x: f"{int(x[0]):02d}{int(x[1]):03d}"
    )
    
    similarity_df = pd.DataFrame(
        similarity, 
        index=state_county_geoids, 
        columns=state_county_geoids
    )
    
    return similarity_df


def get_top_similar_pairs(similarity_df, n=100):
    """
    Extract top N most similar county pairs
    """
    similarity_long = similarity_df.unstack().reset_index()
    similarity_long.columns = ['GEOID_1', 'GEOID_2', 'Similarity']
    
    similarity_long = similarity_long[
        similarity_long['GEOID_1'] != similarity_long['GEOID_2']
    ].sort_values(by='Similarity', ascending=False).head(n)
    
    return similarity_long


def evaluate_clustering_performance(distance_matrix, k_range=range(2, 10)):
    """
    Evaluate clustering performance across different k values
    """
    inertia = []
    silhouette_scores = []
    
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42)
        labels = kmeans.fit_predict(distance_matrix)
        
        inertia.append(kmeans.inertia_)
        silhouette_scores.append(
            silhouette_score(distance_matrix, labels, metric='precomputed')
        )
    
    return {
        'k_values': list(k_range),
        'inertia': inertia,
        'silhouette': silhouette_scores
    }


def plot_clustering_metrics(metrics, save_path=None):
    """
    Plot elbow curve and silhouette scores
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    ax1.plot(metrics['k_values'], metrics['inertia'], marker='o', color='steelblue')
    ax1.set_title("Elbow Method for K-Means", fontsize=14)
    ax1.set_xlabel("Number of Clusters", fontsize=12)
    ax1.set_ylabel("Inertia", fontsize=12)
    ax1.grid(alpha=0.3)
    
    ax2.plot(metrics['k_values'], metrics['silhouette'], marker='o', color='darkorange')
    ax2.set_title("Silhouette Scores for K-Means", fontsize=14)
    ax2.set_xlabel("Number of Clusters", fontsize=12)
    ax2.set_ylabel("Silhouette Score", fontsize=12)
    ax2.grid(alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def perform_clustering(similarity_df, n_clusters=4):
    """
    Perform K-Means clustering on county similarity matrix
    """
    similarity = similarity_df.values
    similarity = (similarity - similarity.min()) / (similarity.max() - similarity.min())
    
    distance_matrix = 1 - similarity
    np.fill_diagonal(distance_matrix, 0)
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(distance_matrix)
    
    clustered_df = pd.DataFrame({
        'GEOID': similarity_df.index,
        'Cluster': labels,
    })
    
    return clustered_df


def analyze_cluster_characteristics(data, clustered_df, feature_cols):
    """
    Calculate mean characteristics for each cluster
    """
    data['GEOID'] = data['STATE'].astype(str).str.zfill(2) + data['COUNTY'].astype(str).str.zfill(3)
    
    merged = data.merge(clustered_df, on='GEOID', how='inner')
    
    cluster_summary = merged.groupby('Cluster')[feature_cols].mean()
    
    return cluster_summary
