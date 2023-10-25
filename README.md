# Patent Analysis Repository

This repository contains a comprehensive set of tools and datasets designed for extracting, processing, analyzing, and visualizing patent data sourced from Lens.org. 

## Repository Structure

- **Scripts**: 
  - `patent_extraction.py`: Extracts patent data from Lens.org using an API key. Each execution produces a JSON output named `raw_output_[YEAR].json`.
  - `merge_output.py`: Aggregates the yearly raw output JSON files into a consolidated `raw_output.json` file. This script is essential as Lens.org restricts data extraction to 10,000 entries per call.

- **Analysis Folder**: 
  - `EDA.ipynb`: Performs Exploratory Data Analysis (EDA) on the patent data, providing useful business insights with graphs plotted.
  - `LDA_and_cluster.ipynb`: Performs Natural Language Processing (NLP) on the patent data to execute topic modeling. This aids in discerning prevalent themes among the patents and clustering them accordingly.
  - `time_series_prediction.ipynb`: Conducts time series analysis on the number of patents over a timeline. It utilizes the ARIMA model to forecast the direction of each patent type one year into the future.

- **Databricks_Pipeline Folder**: 
  - `bronze-flatten.ipynb`: Transforms the raw JSON data into multiple structured PySpark dataframes, especially catering to nested columns with a predetermined schema.
  - `silver-merge.ipynb`: Combines the flattened dataframes into a comprehensive dataframe.
  - `gold1-CPC_mapping.ipynb`: Associates the CPC symbols with their respective class names, culminating in the generation of the first finalized dataset.
  - `gold2-analysis.ipynb`: Facilitates the final data processing, producing the secondary dataset designated for PowerBI.

- **PowerBI_Data Folder**: 
  - Contains two parquet files, the results of the gold-layer notebooks. These files are primed for direct ingestion into PowerBI.

- **Report**: A detailed document providing insights and findings derived from the analyzed patent data.

- **Presentation**: A PowerPoint slide deck that visually communicates the results and conclusions of the patent analysis.

## Usage

1. **Data Extraction**: Execute `patent_extraction.py` to fetch patent data. Subsequently, run `merge_output.py` to aggregate the individual JSON files.
2. **Data Processing**: Upload the notebooks from the `Databricks_Pipeline` folder to orchestrate the complete workflow. The order is bronze - silver - gold.
3. **Data Analysing**: Utilize the notebooks in the `Analysis` folder for topic modeling and time series forecasting. For those leveraging Databricks, upload the notebooks from the `Databricks_Pipeline` folder to orchestrate the complete workflow.
4. **Data Visualization**: Import the parquet files from the `PowerBI_Data` folder into PowerBI for advanced data visualization and dashboard creation.

## Dependencies

- Python Libraries: See requirements.txt
- Python Version: 3.10.11
- Databricks Runtime: DBR 13.3 LTS | Spark 3.4.1 | Scala 2.12



