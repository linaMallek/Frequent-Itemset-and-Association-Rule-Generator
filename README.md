# Frequent Itemsets and Association Rules Generation App

## Overview

This Flask-based application allows users to upload a dataset, apply Apriori-based algorithms to generate frequent itemsets and association rules, and visualize the results. The app generates a bar plot and a PDF with the frequent itemsets and rules.

## Features

- Supports multiple algorithms (classic Apriori, vertical fragment Apriori, and closed itemsets)
- User-specified minimum support, confidence, and lift thresholds
- Generates a bar plot of frequent itemsets
- Outputs association rules and itemsets in a downloadable PDF

## File Structure

- **`app.py`**: The Flask application script.
- **`fct.py`**: Contains the algorithm functions.
- **`templates/`**: Contains HTML templates for rendering.
  - **`upload.html`**: File upload and parameter input form.
  - **`result.html`**: Displays the result, bar plot, and PDF download links.
- **`static/`**: Folder to store generated images and PDFs.
- **`frozensets.txt`**: Temporary file to store frequent itemsets and rules.
- **`frozensets.pdf`**: Generated PDF file with frequent itemsets and association rules.

## Dependencies

- Flask
- Pandas
- Matplotlib
- ReportLab
- NumPy

You can install these dependencies via pip:

```bash
pip install flask pandas matplotlib reportlab numpy
