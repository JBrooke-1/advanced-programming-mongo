import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import files


def analyze_freq_correlation(file_path="data/uk-airports-frequencies.csv"):
    # clean df
    abs_file_path = files.get_parent_folder(file_path)
    freq_df: pd.DataFrame = pd.read_csv(abs_file_path)

    # only keep relevant columns
    freq_df_original = freq_df[["type", "frequency_mhz"]]
    cleaned_freq_df = freq_df[["type", "frequency_mhz"]]
    cleaned_freq_df["type"], uniques = pd.factorize(cleaned_freq_df["type"])
    freq_df_original["codes"] = cleaned_freq_df["type"]
    print("all unique categories are: ", uniques)
    print("after clean the new dataset is: ", cleaned_freq_df.head())

    # analyze the correlation between airport size and frequency
    correlations_pearson = cleaned_freq_df.corr(method="pearson")
    print("pearson correlation matrix \n", correlations_pearson, "\n")

    # visualize correlation in matplotlib
    sns.set_theme(style="darkgrid")
    sns.lmplot(
        x="codes",
        y="frequency_mhz",
        markers=["o", "s", "D"],
        palette="Set1",
        hue="type",
        data=freq_df_original,
    )
    # sns.jointplot(
    #     x="codes",
    #     y="frequency_mhz",
    #     palette="Set1",
    #     kind="reg",
    #     data=freq_df_original,
    # )
    # sns.pairplot(data = freq_df_original,
    # hue = "type",
    # size =3,
    # y_vars = ["frequency_mhz"],
    # x_vars = ["type"],
    #  markers=["o", "s", "D"]
    #  )
    # g = sns.PairGrid(cleaned_freq_df)
    # g.map_diag(sns.histplot)
    # g.map_offdiag(sns.scatterplot)
    # g = sns.FacetGrid(freq_df_original, col="type", hue="type")
    # g.map(sns.kdeplot,"frequency_mhz",
    #             palette="ch:r=-.5,l=.75",)
    # g.map(sns.pointplot,"type", "frequency_mhz", order=["small_airport", "medium_airport", "large_airport"],
    #             palette="ch:r=-.5,l=.75",)
    plt.show()


analyze_freq_correlation()
