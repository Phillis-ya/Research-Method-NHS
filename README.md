# Research Method Coursework2
This repository contains the Python script developed for COMP4037 Research Methods - Coursework 2. The project processes and visualizes the NHS England Hospital Episode Statistics (HES) for admitted patient care (2023-24), using a hierarchical treemap to illustrate the distribution of admissions across different ICD-10 chapters and their subcategories.
Project Overview：
  The primary objective of this project is to reveal the structural characteristics of NHS hospital admissions through data visualization.
    Data Source: NHS England's "Hospital Episode Statistics for Admitted Patient Care, Activity: Diagnosis 2023-24".
    Core Logic:
        Maps complex ICD-10 diagnosis codes into 21 human-readable disease Chapters.
        Extracts the top 5 subcategories with the highest Finished Admission Episodes (FAE) for each chapter.
        Generates both a static image for academic reporting and an interactive webpage for in-depth data exploration.
Prerequisites：
Before running the script, ensure you have Python 3.x installed along with the following required libraries:
