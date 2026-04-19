# Research Method Coursework 2: NHS Hospital Admissions Treemap

## Introduction
Welcome to my submission for the COMP4037 Research Methods Coursework 2. This project focuses on processing and visualizing hospital admission data from the NHS England Hospital Episode Statistics (HES) for the 2023-24 period. 

The main goal of this script is to make complex healthcare data accessible and easy to understand. By generating a hierarchical treemap, it visually breaks down patient admissions across various ICD-10 disease chapters and their specific subcategories, making it easy to see which health conditions account for the most hospital visits.

## Files

* `treemap_visualization.py` : processes the NHS spreadsheet, maps complex ICD-10 diagnosis codes into 21 human-readable Chapters, extracts the top 5 subcategories for each, and generates the hierarchical treemaps.
* `hosp-epis-stat-admi-diag-2023-24-tab.xlsx` : source data file.
* `treemap_nhs.png` : final static visualisation output (high-resolution image, automatically handles text wrapping and dynamic font scaling).
* `treemap_interactive.html` : final interactive visualisation output (powered by Plotly, supports click-to-zoom and hover metrics like FAE, Mean Age, and Length of Stay).

## How the Code Works

### Data Processing Strategy
The script starts by taking the raw, highly technical ICD-10 diagnosis codes and mapping them into 21 human-readable disease chapters (for example, grouping specific codes into broader categories like "Infectious Diseases" or "Neoplasms"). To keep the final visualization clean and readable, it automatically extracts the top 5 subcategories with the highest Finished Admission Episodes (FAE) for each chapter, grouping the remaining smaller categories into an "Others" block.

### Required Libraries
To run this project, you will need Python 3.x installed, along with a few standard data science and visualization packages. You can quickly install everything you need by running the following command in your terminal:

```bash
pip install pandas numpy matplotlib squarify plotly openpyxl
```
### The Dataset
Please ensure you have the data file named `hosp-epis-stat-admi-diag-2023-24-tab.xlsx` saved in the exact same folder as the Python script.

## Running the Project

1. Place both the `treemap_visualization.py` script and your Excel data file in the same folder.
2. Open your terminal, navigate to that folder, and run:
   `python treemap_visualization.py`
3. The script will save two new visualization files in your folder.

## Project Outputs

### 1. Static Treemap (treemap_nhs.png)
A high-resolution static image. It uses a custom hierarchical color palette and handles text wrapping automatically.

### 2. Interactive Treemap (treemap_interactive.html)
An interactive HTML webpage (open in any browser). It features click-to-zoom and reveals metrics like FAE, Mean Age, and Length of Stay on hover.
