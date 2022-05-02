import pandas as pd
import os
import files

def analyze_freq_correlation(file_path="data/uk-airports-frequencies.csv"):
    # clean df
    abs_file_path = files.get_parent_folder(file_path)
    freq_df: pd.DataFrame = pd.read_csv(abs_file_path)
    
    # only keep relevant columns
    cleaned_freq_df = freq_df[["type", "frequency_mhz"]]
    cleaned_freq_df["type"],uniques = pd.factorize(cleaned_freq_df["type"])
  
    print("all unique categories are: ", uniques)
    print("after clean the new dataset is: ", cleaned_freq_df.head())
    
    # analyze the correlation between airport size and frequency
    correlations_pearson = cleaned_freq_df.corr(method='pearson')
    print("pearson correlation matrix \n", correlations_pearson, "\n")
    
analyze_freq_correlation()