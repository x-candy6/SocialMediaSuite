# To use this in a subfolder:
#import sys
#sys.path.append('..')
#import helper
import logging
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import seaborn as sns
import mysql.connector
import matplotlib.pyplot as plt
import json
import requests
import sys



def list_options():
    print("hi")
    return

def list_help():
    print("hi")
    return

def get_db(config):
    connection = mysql.connector.connect(
        host=config["database"]["host"],
        user=config["database"]["username"],
        password=config["database"]["password"],
        database=config["database"]["db_name"]
    )
    return (connection, connection.cursor())


#For prod
#dataframes = helper.load_csv(helper.select_files(), None, False)

def select_file():
    file_path = filedialog.askopenfile()  # Open file dialog for multiple files
    return file_path
def select_files():
    file_paths = filedialog.askopenfilenames()  # Open file dialog for multiple files
    for path in file_paths:
        print(f"Selected {path}")
    
    return file_paths

def select_folders():
    folder_paths = []
    while True:
        folder_path = filedialog.askdirectory()  # Open folder dialog to select a folder
        if not folder_path:  # If user cancels selection, exit the loop
            break
        folder_paths.append(folder_path)
    print("Selected folders:")
    for path in folder_paths:
        print(path)
    return folder_paths

def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def write_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    return file

# Networking
def test_request(link, parameters=None):
    response = requests.get(link)
    if response.status_code == 200:
        print("Request successful!")
        print("Response content:")
        print(response.text)
    else:
        print("Request failed with status code:", response.status_code)

def setup_logging():
## Usage
#logger = helper.setup_logging()
#logger.debug('This is a debug message')
#logger.info('This is an info message')
#logger.warning('This is a warning message')
#logger.error('This is an error message')
#logger.critical('This is a critical message')
    # Create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Set logger level to DEBUG

    # Create console handler and set level to DEBUG
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add formatter to handler
    ch.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(ch)

    return logger


#dtype: Dict - For columns with mixed datatypes. Each key is the column indice and value is the datatype
def load_csv(selected_files, dtype=None, low_memory=True):
    dataframes = []
    for file in selected_files:
        if low_memory == False:
            df = pd.read_csv(file, low_memory=False)
            print(f"Sanitizing Data for {file}")
            df = sanitize_csv(df)
            print("Sanitization Completed.")
        else:
            df = pd.read_csv(file)
            print(f"Sanitizing Data for {file}")
            df = sanitize_csv(df)
            print("Sanitization Completed.")
        dataframes.append(df)
        print(f"{file} has been loaded.")

    return dataframes


def sanitize_csv(df):
    # Read the CSV file into a pandas DataFrame
    
    # Handle missing values
    df.fillna(value=0, inplace=True)  # Replace NaN values with 0 (adjust as needed)
    
    # Remove duplicate rows
    #df.drop_duplicates(inplace=True)
    
    # Convert data types (adjust as needed)
    #df['column_name'] = df['column_name'].astype(str)  # Convert a column to string type
    
    # Remove leading and trailing whitespaces from string columns
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)    
    df = pd.get_dummies(df)
    return df

# Correlation Matrix
#    The diagonal elements represent the correlation of each variable with itself, which is always 1 (perfect correlation).
#    Off-diagonal elements represent the correlation between pairs of variables.
#    Correlation coefficients range from -1 to 1:
#        1 indicates a perfect positive correlation, meaning that as one variable increases, the other variable also increases proportionally.
#        -1 indicates a perfect negative correlation, meaning that as one variable increases, the other variable decreases proportionally.
#        0 indicates no linear correlation between the variables.
def construct_correlation_matrix(df, show=False):
    # Compute correlation matrix
    correlation_matrix = df.corr()

    # Plot correlation matrix heatmap
    if show == True:

        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, linecolor='black')
        plt.title('Correlation Matrix')
        plt.show()

    return correlation_matrix


#if len(sys.argv) != 2:
#    print("Usage: python script.py <function>")
#    sys.exit(1)
#func_name = sys.argv[1]
#if func_name == "help":
#    list_help()
#elif func_name == "options":
#    list_options()


# Analyzing the Correlation Matrix
# 1. Identify Strong Correlations
# 2. Check for Weak Correlations
# 3. Visualize the Correlation Matrix
# 4. Identify Multicollinearity
# 5. Consider the Significance of Correlations
# 6. Interpret Negative Correlations
# 7. Review Domain Knowledge
# 8. Evaluate Outliers and Influential Observations
# 9. Perform Sensitivity Analysis



### ARCHIVE ###

# Dynamic Graph Sizes
#        # Create a Tkinter window to get screen resolution
#        root = tk.Tk()
#        screen_width = root.winfo_screenwidth()
#        screen_height = root.winfo_screenheight()
#        root.destroy()
#
#        # Calculate figure size based on screen resolution
#        fraction_of_screen = 0.8  # Adjust as needed
#        width = screen_width * fraction_of_screen
#        height = screen_height * fraction_of_screen