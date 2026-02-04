# Analyzing Economic and Demographic Factors in U.S. Grocery Store Availability

## TLDR
A data driven analysis of how economic conditions, demographics, and spatial connectivity shape grocery store availability across U.S. counties from 2019 to 2022  
By integrating Census population data, county business patterns, and geographic networks, this project applies statistical testing, clustering, and PageRank based spatial analysis to uncover structural drivers of food deserts, showing that economic vitality and regional connectedness matter more than raw population size alone

---

## Objective
The goal of this project is to examine how economic, demographic, and geographic factors influence grocery store access across U.S. counties and to identify regions that may be at higher risk of food insecurity

Specifically, the project aims to
- Measure relationships between income, employment, demographics, and grocery availability  
- Identify clusters of counties with similar socioeconomic and retail characteristics  
- Evaluate the role of spatial and regional economic connectivity using network metrics  
- Provide data driven insights relevant to food equity research  

---

## Data Sources

| Dataset | Source | Description |
|-------|--------|-------------|
| County Population Estimates | U.S. Census Bureau | County level population by age, gender, and race |
| County Business Patterns | U.S. Census Bureau | Grocery establishments, employment, payroll by size |
| TIGER Line Shapefiles | U.S. Census Bureau | County boundaries and land area |
| Derived Metrics | Computed | Grocery density, employment per area, PageRank |

The dataset covers 2019 to 2022 and includes over 3,000 U.S. counties

---

## Methodology

### 1. Data Preprocessing
- Loaded and merged population, grocery establishment, and land area datasets by county and year  
- Cleaned and standardized identifiers for consistent joins  
- Engineered normalized indicators including
  - Grocery establishments per capita  
  - Employment and payroll per land area  
  - Demographic percentage breakdowns  

### 2. Exploratory and Statistical Analysis
- Visualized temporal trends in grocery availability across years  
- Computed correlations between grocery access and socioeconomic variables  
- Conducted t tests and ANOVA to compare at risk and non at risk counties  

### 3. Clustering Analysis
- Standardized county level features related to income, employment, demographics, and grocery density  
- Applied clustering techniques to group counties with similar profiles  
- Interpreted clusters in the context of food access inequality  

### 4. Network and Spatial Analysis
- Built a county adjacency network based on shared geographic borders  
- Weighted edges using economic indicators to reflect regional spillover effects  
- Applied the PageRank algorithm to estimate each county’s regional economic influence  

---

## Key Insights

| Insight | Interpretation |
|-------|----------------|
| Grocery access is strongly correlated with payroll and employment density | Economic vitality is a stronger driver than population size |
| Counties cluster into distinct socioeconomic grocery access profiles | Food access inequality is structurally patterned |
| Economically isolated counties tend to have weaker grocery ecosystems | Regional connectivity supports retail sustainability |
| Food deserts show clear geographic clustering | Food insecurity is not randomly distributed |
