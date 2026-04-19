# RESEARCH METHOD COURSEWORK 2: NHS HOSPITAL ADMISSIONS TREEMAP VISUALIZATION

[Project Overview]

This repository contains the Python script developed for COMP4037 Research Methods - Coursework 2. The project processes and visualizes the NHS England Hospital Episode Statistics (HES) for admitted patient care (2023-24). It uses a hierarchical treemap to illustrate the distribution of admissions across different ICD-10 chapters and their subcategories.

[Core Logic]

    Maps complex ICD-10 diagnosis codes into 21 human-readable disease Chapters.

    Extracts the top 5 subcategories with the highest Finished Admission Episodes (FAE) for each chapter.

    Generates both a static image for academic reporting and an interactive webpage for in-depth data exploration.

[Prerequisites]

Before running the script, ensure you have Python 3.x installed along with the following required libraries. You can install them in your terminal using this command:
pip install pandas numpy matplotlib squarify plotly openpyxl

    pandas: Data cleaning, filtering, and hierarchical structure building.

    matplotlib: Generating high-resolution static PNG images.

    squarify: Calculating the treemap layout algorithm.

    plotly: Generating interactive HTML with zoom and hover capabilities.

    openpyxl: Engine required by pandas to read Excel files.

[Data Requirements]

The script requires a specific NHS data file to function. Please ensure the following file is placed in the exact same directory as the script:

    Filename: hosp-epis-stat-admi-diag-2023-24-tab.xlsx

    Target Sheet: Primary Diagnosis Summary

[How to Run]

    Place the files: Ensure treemap_visualization.py and the Excel data file are in the same folder.

    Execute the script: Open your terminal or command prompt and run: python treemap_visualization.py

    Check the output: The console will confirm once the visualization files have been successfully saved in your folder.

[Visualization Outputs]

    Static Treemap (treemap_nhs.png): Uses a hierarchical color palette where different colors represent distinct ICD-10 Chapters. Automatically handles text wrapping and dynamic font scaling. Ideal for embedding directly into Word documents, academic papers, or slide presentations.

    Interactive Treemap (treemap_interactive.html): Powered by Plotly, supporting click-to-zoom (drill-down) functionality for specific chapters. Hovering over a block reveals detailed metrics like Total Admissions (FAE), Emergency Ratio, Mean Age, and Mean Length of Stay.
