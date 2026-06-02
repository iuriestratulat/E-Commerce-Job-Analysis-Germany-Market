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

A comprehensive analysis of the **German E-Commerce job market** based on **1,581 real job postings** from LinkedIn, Glassdoor, and Stepstone (October 2025).

### 🎯 Key Questions Answered

| Question | Insight |
|----------|---------|
| **Where** are the main e-commerce job hubs? | Berlin (391 jobs), Hamburg, Munich, Cologne |
| **What** are the most requested skills? | Marketing (64%), E-Commerce (57%), Management (39%) |
| **How** do skills change by seniority? | Entry level focuses on Marketing; Executive requires Leadership |
| **What** is the market trend? | Steady growth over the last 6 months |
| **Who** are the top employers? | Amazon, Zalando, Delivery Hero, Westwing |

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
- **Month/Date Range** (for trends)

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
e-commerce-job-analysis/
├── dashboard/ # Plotly Dash application
│ ├── app.py # Main Dash application
│ ├── data_loader.py # Data loading utilities
│ ├── components/ # Reusable Dash components
│ ├── assets/ # CSS and static assets
│ ├── data/ # Processed dataset (1,581 jobs)
│ └── requirements.txt # Python dependencies
│
├── ecommerce_pipeline/ # ETL Pipeline
│ └── e_commerces_etl.py # Complete data processing pipeline
│
├── notebooks/ # Jupyter notebooks for analysis
│ ├── E_Commers_Analysis.ipynb
│ ├── Title_and_description.ipynb
│ └── LinkedIn_Parser.ipynb
│
└── runway/ # Legacy/backup files (git ignored)

---

## 📈 Key Findings

### 🏙️ Top Hiring Cities
| City | Jobs | % of Total |
|------|------|-------------|
| Berlin | 391 | 24.7% |
| Hamburg | ~150 | ~9.5% |
| Munich | ~120 | ~7.6% |
| Cologne | ~80 | ~5.1% |

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

### 🎓 Recommendations for Graduates
1. **Invest in Digital Marketing & Google Analytics**
2. **Learn E-Commerce fundamentals** (platforms, logistics, customer journey)
3. **German language is a major differentiator**
4. **Target roles:** Online Marketing Manager, E-Commerce Specialist

### 💰 Salary Progression (E-Commerce Track)
| Stage | Salary (€K) |
|-------|-------------|
| Entry Level | 38-48 |
| Junior | 48-55 |
| Mid-Level | 55-70 |
| Senior | 70-90+ |
| Lead/Manager | 90-120+ |

---

## 🚀 Local Setup for interactive dashboard

### Prerequisites
- Python 3.13+
- pip package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/iuriestratulat/e-commerce-job-analysis.git
cd e-commerce-job-analysis

# Navigate to dashboard
cd dashboard

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
python app.py 

```

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