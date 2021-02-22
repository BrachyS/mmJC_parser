# mmJC_parser
 Parser and exporter for the mmJC csv files, along with a db schema to store/query the data

**System requirements**:
Tested under Mac OS (Version 10.13.6), python 3.6
Packages required:
'pandas >= 1.1.3',
'numpy >= 1.18.1',
'openpyxl >= 3.0.6'


## Installation
In command line, do:
1. Navigate to the file folder ../mmJC_parser
2. > pip install .

# Running a sample code
In command line:
1. Navigate to the file folder
2. Put the two sample data files in folder: data/raw/
3. > python sample_run.py

# Running the tests
In command line:
1. Navigate to the file folder
2. > pytest

# Methods (Workflow):

1. Reshape data from wide into long format and remove missing values stored in 'records'
2. Identify outliers and remove them (i.e., treat as missing values)
3. Subset LH into a separate table because it is text data rather than numeric
4. Reshape cleaned data from long format back into wide format, downsampling time intervals
(also help resolve inconsistent missing values across different times) for easy plotting
5. Export to Excel and CSV files (for database, following the schema designed)

Link to schema:
https://dbdiagram.io/d/6032ba00fcdcb6230b20d17b

More notes and my work process can be find in the jupyter notebook
/notebooks/'data_wrangling.ipynb'


# Todo
1. The resulting files still contain some missing values, though much fewer than the raw file
We could consult the client if further removing those missing values are necessary, and what are good methods.
For example, can we aggregate data on bigger time intervals? Should we impute missing values or replace with mean?

2. I did not use a standard criteria (e.g., 1.5*IQR) to check outliers, and simply removed a few obvious ones I spotted.
We should ask the client what criteria is appropriate for defining outliers

3. Due to time limit, the unit tests are incomplete. More testing are needed.

4. We can automate this process, so that when a new data file is uploaded, the parser can recognize it and parse it correctly.

5. Do the output files satisfy the clients' needs? Need further discussions

