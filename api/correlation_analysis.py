import pandas as pd
import os
import files

def analyze_freq_correlation(file_path="data/uk-airport-frequencies.csv"):
    abs_file_path = files.get_parent_folder(file_path)
    print(abs_file_path)