# Analyzing Economic and Demographic Factors in U.S. Grocery Store Availability

## TLDR
A data-driven investigation into how **economic vitality and demographic diversity influence grocery store availability** across U.S. counties (2019–2022).  
By integrating Census datasets and applying **regression, clustering, and PageRank-based network analysis**, we uncovered structural patterns behind **food deserts** — showing that **economic health and spatial connectivity** play a larger role in grocery access than population size or racial composition.

---

## Objective
To analyze the relationship between **economic, demographic, and spatial factors** and **grocery store accessibility** across the United States, and to identify **counties at risk of food insecurity**.

Specifically:
- Quantify how income, employment, and population diversity correlate with grocery availability  
- Detect clusters of counties with similar socioeconomic profiles  
- Use network-based metrics (PageRank) to evaluate **regional economic influence**  
- Provide actionable insights for policymakers to improve food equity  

---

## Data Sources

| Dataset | Source | Key Features |
|----------|---------|---------------|
| County Business Patterns | U.S. Census Bureau | Grocery store counts, employment, payroll |
| American Community Survey | U.S. Census Bureau | Demographics, income, age, race, population |
| U.S. County Shapefiles | Census TIGER/Line | Geographic boundaries |
| Derived Metrics | Computed | Grocery density, payroll per capita, PageRank influence |

Data spans **2019–2022** with 3,000+ U.S. counties.

---

## Methodology

### **1. Data Preprocessing**
- Cleaned and merged multiple Census datasets by county and year  
- Computed derived indicators such as:
  - Grocery stores per 10,000 residents  
  - Payroll per area  
  - Employment density  
- Normalized features for fair comparison across counties  

### **2. Exploratory & Statistical Analysis**
- Time-series visualization of grocery availability trends (2019–2022)  
- Correlation matrix and regression modeling to identify key drivers  
- T-tests and ANOVA comparing “at-risk” vs. “stable” grocery regions  

### **3. Clustering Analysis**
- Applied **K-Means** to standardized socioeconomic features  
- Identified clusters of counties with similar income, employment, and diversity patterns  
- Visualized cluster assignments using geographic mapping  

### **4. Network & Spatial Analysis**
- Constructed a **county adjacency graph** based on geographic boundaries  
- Weighted edges using **payroll per area** to capture local economic spillovers  
- Applied **PageRank algorithm** to measure each county’s **regional economic influence**  
- Interpreted low-PageRank counties as **economically isolated** and more vulnerable to food deserts  

---

## Key Insights

| Finding | Interpretation |
|----------|----------------|
| Counties with lower payroll and employment density have fewer grocery stores | Economic vitality is the primary determinant of grocery access |
| Racially diverse and urban counties tend to have stronger grocery ecosystems | Diversity correlates with retail density and consumer demand |
| High-PageRank (economically connected) counties maintain better store access | Regional economic influence sustains grocery availability |
| Food deserts cluster geographically, often in low-income, low-connectivity areas | Structural inequity drives grocery distribution patterns |

---

## Policy Implications
- Prioritize **investment and incentives** in low-PageRank, low-income counties  
- Support **regional economic integration** to stabilize grocery access  
- Use PageRank as a scalable, data-driven **food insecurity risk index**  
- Extend the model to incorporate **transportation and rural infrastructure data**

---

