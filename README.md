# Grocery Store Food Desert Analysis

A comprehensive geospatial and demographic analysis system for identifying and characterizing food deserts across U.S. counties using clustering, network analysis, and statistical hypothesis testing.

## Project Overview

This project analyzes grocery store accessibility patterns across 3,000+ U.S. counties using multi-source data integration (Census demographics, County Business Patterns, USDA Food Access metrics) to identify at-risk regions, quantify demographic disparities, and reveal spatial propagation patterns through network analysis.

## Key Highlights

- **Dataset**: 14,000+ county-year observations (2019-2022) across 3,142 counties
- **Clustering**: K-Means segmentation (k=4, silhouette=0.38) identifying distinct county types
- **Network Analysis**: PageRank scores on 9,800+ county adjacency edges
- **Statistical Testing**: Correlation analysis, t-tests, ANOVA revealing demographic disparities
- **Key Finding**: -0.42 correlation between Native American population and establishment density

## Dataset

### Core Data Sources
- **U.S. Census Bureau**: County population estimates (2019-2022)
  - Demographics: Age groups (18 brackets), Race/Ethnicity (6 categories)
  - Totals: Population, Male/Female counts
- **County Business Patterns (CBP)**: Grocery establishment data (NAICS 445)
  - Metrics: Establishment counts by size, Employment, Annual payroll
  - Granularity: 9 establishment size categories (1-4, 5-9, ..., 1000+)
- **TIGER/Line Shapefiles**: County boundaries and land area
- **USDA Food Access Research Atlas**: Low-access tract indicators, poverty rates, median income


### Engineered Features
- **Demographic**: Race/ethnicity percentages, gender ratios
- **Economic**: Establishments/km², employees/km², payroll/km²
- **Temporal**: Absolute and percentage changes (2019→2022)
- **Derived**: At-risk indicator, bed utilization ratios


## Usage

### Basic Analysis
```python
from src.data_processing import load_and_merge_data
from src.feature_engineering import calculate_demographic_percentages
from src.clustering import perform_clustering

# Load data
data = load_and_merge_data(
    population_file='data/cc-est2023-alldata.csv',
    grocery_years=[2019, 2020, 2021, 2022]
)

# Engineer features
data, pct_cols = calculate_demographic_percentages(data)

# Perform clustering
clusters = perform_clustering(similarity_matrix, n_clusters=4)
```

### Network Analysis
```python
from src.spatial_analysis import build_adjacency_graph, calculate_pagerank

# Build county adjacency network
adjacency_df, graph = build_adjacency_graph('data/tl_2018_us_county.shp')

# Calculate PageRank scores
pagerank_df, top_county = calculate_pagerank(network_data, 'EMP')
```

### Statistical Testing
```python
from src.statistical_tests import calculate_correlations, t_test_at_risk_vs_safe

# Correlations with establishment density
corr_df = calculate_correlations(data, 'ESTAB_All/Area', demographic_features)

# Compare at-risk vs safe counties
t_test_results = t_test_at_risk_vs_safe(data, 'At_Risk', 'MedianFamilyIncome')
```

## Methodology

### 1. Data Integration
- Merge Census population, CBP grocery data, TIGER shapefiles
- Harmonize FIPS codes, handle missing values
- Engineer 100+ temporal, demographic, economic features

### 2. Clustering Analysis
- **Preprocessing**: PCA dimensionality reduction (358→85% variance)
- **Algorithm**: K-Means with elbow method + silhouette scoring
- **Optimal k**: 4 clusters (silhouette=0.38)
- **Results**: 
  - Cluster 0 (38%): Rural agricultural, low density, declining
  - Cluster 1 (24%): Suburban growth, moderate density
  - Cluster 2 (29%): Urban diverse, high density
  - Cluster 3 (9%): Indigenous-majority, critical shortage

### 3. Spatial Network Analysis
- **Graph Construction**: County adjacency from shapefile geometry
- **Nodes**: 3,142 counties
- **Edges**: 9,800+ touching boundaries
- **PageRank**: Weighted by establishment density/employment
- **Centrality**: Degree centrality identifies high-connectivity hubs

### 4. Statistical Hypothesis Testing
- **Correlations**: Pearson r between demographics and establishment metrics
  - Native American %: r = -0.42 (p < 0.001)
  - Poverty Rate: r = -0.51 (p < 0.001)
  - Median Income: r = +0.56 (p < 0.001)
- **T-Tests**: At-risk vs adequately served counties
- **ANOVA**: Variation across demographic groups
- **Temporal**: Population change vs establishment density change (r = 0.34)

## Key Results

### Cluster Characteristics
| Cluster | Counties | Type | Establishment Density | Population Trend | Median Income |
|---------|----------|------|----------------------|-----------------|---------------|
| 0 | 38% | Rural Agricultural | <0.0005/km² | Declining (-3%) | $48K |
| 1 | 24% | Suburban Growth | 0.002-0.004/km² | Growing (+5%) | $68K |
| 2 | 29% | Urban Diverse | >0.005/km² | Stable/Growing | $78K |
| 3 | 9% | Indigenous-Majority | <0.0003/km² | Declining (-10%) | $38K |

### Top PageRank Counties
1. **Los Angeles County, CA**: PageRank 0.042 (250K+ employees, urban anchor)
2. **Cook County, IL**: PageRank 0.038 (Chicago metro, Midwest hub)
3. **Harris County, TX**: PageRank 0.034 (Houston region, rapid growth)

### Demographic Disparities
- **Native American population**: -0.42 correlation with establishment density
- **Black population**: -0.18 correlation
- **Poverty rate**: -0.51 correlation (higher poverty → less access)
- **At-risk counties**: 18.2% poverty vs 11.4% for served counties (p < 0.001)

## Policy Implications

1. **Targeted Interventions by Cluster**:
   - Cluster 0: Mobile markets, transportation assistance
   - Cluster 3: Tribal enterprise support, federal funding
   - Clusters 1-2: Monitor for gentrification displacement

2. **Network-Based Strategies**:
   - Strengthen high-PageRank anchor counties
   - Regional food hub development for spillover benefits

3. **Addressing Disparities**:
   - Environmental justice programs for Indigenous/Black-majority counties
   - Incentives for grocery investment in high-poverty areas

4. **Market Failure Correction**:
   - Zoning reforms for growing counties lacking grocery expansion
   - Tax incentives to reduce 0.34 population-establishment gap

## Challenges & Limitations

1. **Data Quality**: Missing establishment counts for smallest size categories
2. **Threshold Selection**: At-risk cutoff (0.001/km²) somewhat arbitrary
3. **Causality**: Correlations don't prove causal mechanisms
4. **Temporal Scope**: 2019-2022 limited to detect long-term trends
5. **Spatial Resolution**: County-level masks intra-county variation (urban vs rural areas)

## Future Enhancements

- [ ] Incorporate transportation network data (drive times to nearest grocery)
- [ ] Add SNAP/WIC program participation as covariate
- [ ] Time-series forecasting for at-risk county identification
- [ ] Mobile app for real-time food desert mapping
- [ ] Integration with farmers market and food pantry locations
- [ ] Machine learning models for risk prediction (Logistic Regression, Random Forest, XGBoost)
- [ ] SHAP analysis for model interpretability
- [ ] Geospatial visualization dashboard (Folium, Plotly)
