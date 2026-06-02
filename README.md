# 📊 E-Commerce Job Market Dashboard - Germany 2025

[![Live Demo](https://img.shields.io/badge/Live_Demo-https://e--commerce--job--analysis.onrender.com-2ea44f?style=for-the-badge&logo=render)](https://e-commerce-job-analysis.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.13-blue.svg?style=flat&logo=python)](https://www.python.org/)
[![Dash](https://img.shields.io/badge/Dash-2.16.0-blue.svg?style=flat&logo=plotly)](https://plotly.com/dash/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat)](LICENSE)

## 🚀 Live Dashboard

**👉 [Click to view the interactive dashboard](https://e-commerce-job-analysis.onrender.com)**

> ⚡ *Note: The first load may take 15-30 seconds as the free tier service wakes up.*

---

## 📋 Project Overview

A comprehensive analysis of the **German E-Commerce job market** based on **1,581 cleaned job postings** aggregated from LinkedIn, Glassdoor, and Stepstone. The project monitors market dynamics over a 6-month period culminating in October 2025.

### 🎯 Key Questions Answered

| Question | Analytical Goal |
|----------|-----------------|
| **Where** are the main e-commerce job hubs? | Identify the top hiring cities and regional job density across Germany. |
| **What** are the most requested skills? | Map the core technical capabilities and soft skills required by employers. |
| **How** do skills change by seniority? | Analyze skill requirements across different career stages (Entry vs. Executive). |
| **What** is the market trend? | Track the volume and stability of job postings over a 6-month timeline. |
| **Who** are the top employers? | Discover the major companies driving the e-commerce recruitment market. |

---

## 📊 Dashboard Features

### 7 Interactive Tabs

| Tab | Content |
|-----|---------|
| 📊 **Overview** | Total jobs, top skills, contract types, top companies |
| 🗺️ **Geographic Analysis** | Job distribution by region and city (interactive maps) |
| 🔧 **Skills Analysis** | Most in-demand skills (Treemap + Heatmap) |
| 📋 **Job Distribution** | Experience levels, contract types, work types |
| 📈 **Career Progression** | Career paths and salary progression |
| 📈 **Trends** | Weekly job posting trends (last 6 months) |
| 🎓 **Conclusions** | Key takeaways and recommendations for graduates |

### 🔍 Interactive Filters

- **Experience Level** (Entry, Mid-Senior, Executive, etc.)
- **Contract Type** (Full-time, Part-time, Internship)
- **Month/Date Range** (for trends exploration)

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Dashboard** | Plotly Dash, Dash Bootstrap Components |
| **Data Processing** | Python, Pandas, NumPy |
| **Visualization** | Plotly, Mapbox, Heatmaps, Treemap, Sankey |
| **ETL Pipeline** | Python, JSON, Regex |
| **Deployment** | Render.com |
| **Version Control** | Git, GitHub |

---

## 📁 Project Structure

```text
e-commerce-job-analysis/
├── dashboard/                              # Plotly Dash interactive dashboard
│   ├── components/                         # Reusable Dash UI components
│   │   ├── career_components.py            # Career progression visualizations
│   │   ├── map_components.py               # Geographic maps (choropleth, bubble)
│   │   ├── skills_components.py            # Skills analysis (treemap, heatmap)
│   │   └── temporal_components.py          # Time-based trends charts
│   ├── assets/                             # Static files
│   │   └── style.css                       # Custom CSS styling
│   ├── data/                               # Dashboard datasets
│   │   ├── city_coordinates.json           # City coordinates for maps
│   │   └── E_Commers_jobs_done.json        # Final cleaned dataset (1,581 jobs)
│   ├── app.py                              # Main Dash application entry point
│   ├── data_loader.py                      # Data loading utilities
│   └── requirements.txt                    # Python dependencies
│
├── ecommerce_pipeline/                                 # ETL data processing pipeline
│   ├── data/                                           # Data storage
│   │   ├── helpers/                                    # Helper files for data processing
│   │   │   ├── unique_skills_combined.json             # Master list of unique skills (605)
│   │   │   ├── job_title.json                          # Relevant job titles for filtering
│   │   │   ├── statistics.json                         # Generated statistics from analysis
│   │   │   └── location_reports/                       # Location analysis reports
│   │   │       ├── incomplete_locations.json           # Jobs missing region data
│   │   │       └── location_analysis.json              # Location format analysis
│   │   ├── processed/                                  # Cleaned, step-by-step data
│   │   │   ├── 01_e_commers_jobs.json                  # Step 1: Raw normalized jobs
│   │   │   ├── 02_e_commers_jobs_with_skills.json      # Step 2: Skills extracted
│   │   │   ├── 03_e_commers_jobs_filtered.json         # Step 3: Filtered by title
│   │   │   ├── 04_e_commers_jobs_locations_split.json  # Step 4: Locations split
│   │   │   └── 05_e_commers_jobs_final.json            # Step 5: Final clean data
│   │   └── raw/                                        # Raw source data
│   │       ├── dataset_linkedin_e_com.json             # LinkedIn raw jobs
│   │       ├── dataset_glassdoor_e_com.json            # Glassdoor raw jobs
│   │       └── dataset_stepstone_e_com.json            # Stepstone raw jobs
│   └── e_commerces_etl.py                              # Complete ETL pipeline script
│
├── notebooks/                                          # Jupyter notebooks for exploration
│   └── E_Commers_Analysis.ipynb                        # Main analysis notebook
│
├── runway/                                             # Legacy/backup files (git ignored)
├── .gitignore                                          # Git ignore rules
└── LICENSE                                             # MIT License
 ```

---

## 📈 Key Findings

### 🏙️ Top Hiring Cities
| City | Jobs | % of Total |
|------|------|-------------|
| Berlin | 391 | 24.7% |
| Hamburg | ~150 | ~9.5% |
| Munich | ~120 | ~7.6% |
| Cologne | ~80 | ~5.1% |

```text
Primary Employers: Amazon, Zalando, Delivery Hero, Westwing.
```

### 🔧 Most In-Demand Skills
| Skill | % of Jobs |
|-------|------------|
| Marketing | 64.3% |
| E-Commerce | 57.3% |
| Management | 38.9% |
| IT | 24.9% |
| Sales | 24.3% |

### 📝 Contract Types
- **Full-time:** 84%
- **Part-time:** 9%
- **Contract:** 7%

### 💰 Salary Progression (E-Commerce Track)
| Stage | Salary (€K) |
|-------|-------------|
| Entry Level | 38-48 |
| Junior | 48-55 |
| Mid-Level | 55-70 |
| Senior | 70-90+ |
| Lead/Manager | 90-120+ |

### 🎓 Recommendations for Graduates
1. **Invest in Digital Marketing & Google Analytics**
2. **Learn E-Commerce fundamentals** (platforms, logistics, customer journey)
3. **German language is a major differentiator**
4. **Target roles:** Online Marketing Manager, E-Commerce Specialist
---

## 🔧 ETL Pipeline

The ETL (Extract, Transform, Load) pipeline automates the entire data processing workflow:

1. **Extract**: Collects raw JSON data from LinkedIn, Glassdoor, and Stepstone
2. **Transform**: Normalizes fields, extracts skills from job descriptions using regex, filters jobs from the last 6 months, and splits locations into city/region/country
3. **Load**: Saves cleaned data into structured JSON files ready for the dashboard

The pipeline processes **5,178 raw job postings** and outputs **1,581 high-quality, filtered jobs** ready for analysis.

### Run the Pipeline

```bash
cd ecommerce_pipeline
python e_commerces_etl.py
```

## 🚀 Local Setup for interactive dashboard

### Prerequisites
- Python 3.13+
- pip package manager

### Installation

```bash
# Clone the repository
git clonehttps://github.com/iuriestratulat/E-Commerce-Job-Analysis-Germany-Market.git
cd e-commerce-job-analysis

# Navigate to dashboard
cd dashboard

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
python app.py 
```

