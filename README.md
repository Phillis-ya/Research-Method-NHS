# Research Method Coursework 2: NHS Hospital Admissions Treemap

## Introduction
Welcome to my submission for the COMP4037 Research Methods Coursework 2. This project focuses on processing and visualizing hospital admission data from the NHS England Hospital Episode Statistics (HES) for the 2023-24 period. 

The main goal of this script is to make complex healthcare data accessible and easy to understand. By generating a hierarchical treemap, it visually breaks down patient admissions across various ICD-10 disease chapters and their specific subcategories, making it easy to see which health conditions account for the most hospital visits.

## How the Code Works

### Data Processing Strategy
The script starts by taking the raw, highly technical ICD-10 diagnosis codes and mapping them into 21 human-readable disease chapters (for example, grouping specific codes into broader categories like "Infectious Diseases" or "Neoplasms"). To keep the final visualization clean and readable, it automatically extracts the top 5 subcategories with the highest Finished Admission Episodes (FAE) for each chapter, grouping the remaining smaller categories into an "Others" block.

### Required Libraries
To run this project, you will need Python 3.x installed, along with a few standard data science and visualization packages. You can quickly install everything you need by running the following command in your terminal:

```bash
pip install pandas numpy matplotlib squarify plotly openpyxl

The Dataset

The script is built to process the official NHS statistics. Please ensure you have the data file named hosp-epis-stat-admi-diag-2023-24-tab.xlsx saved in the exact same folder as the Python script. The code will automatically locate and read from the "Primary Diagnosis Summary" sheet.
Running the Project

Getting the visualizations is very straightforward:

    1.Place both the treemap_visualization.py script and your Excel data file in the same folder.

    2.Open your terminal or command prompt, navigate to that folder, and run the script using:
    python treemap_visualization.py

    3.The script will process the data and automatically save two new visualization files in your folder.

Project Outputs
1. Static Treemap (treemap_nhs.png)

The script generates a high-resolution static image. It uses a custom hierarchical color palette where each color represents a distinct ICD-10 chapter. The code automatically handles text wrapping and dynamic font scaling so the labels fit neatly inside their respective boxes. This version is perfect for embedding directly into academic reports, Word documents, or presentation slides.
2. Interactive Treemap (treemap_interactive.html)

For a more in-depth exploration of the data, the script also creates an interactive HTML webpage powered by Plotly. You can open this file in any standard web browser. It features click-to-zoom (drill-down) functionality, and if you hover your cursor over any specific block, it reveals exact metrics: the total admissions (FAE), the emergency admission ratio, the mean age of the patients, and their average length of stay in the hospital.
