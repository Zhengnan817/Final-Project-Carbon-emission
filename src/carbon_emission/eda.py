"""
This module facilitates the retrieval of CO2 emissions data from the EIA API and provides functionality for data preparation to enable visualization. It offers two distinct classes:

- APIReader: This class is designed to retrieve CO2 emissions data from the EIA API. To utilize this class, users need to obtain an API key from https://www.eia.gov/opendata/register.php and provide it during class initialization.
- DataPrep: This class focuses on preparing and processing the data for visualization purposes.

This class, EDAPerformer, facilitates various visualization methods to explore single-column analysis in a DataFrame.

Dependencies:
- seaborn
- matplotlib.pyplot
- geopandas
- requests
- matplotlib.patches
- requests.exceptions.HTTPError

The module relies on various dependencies including requests, pandas, tqdm, matplotlib.pyplot, seaborn, and geopandas to effectively manage data retrieval, processing, and visualization tasks.
"""

import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
import requests
import matplotlib.patches as mpatches
from requests.exceptions import HTTPError


class EDAPerformer:
    """
    This class is for the single columns analysis in the EDA.
    """

    def __init__(self, df):
        """
        Initialize EDAPerformer class with the input DataFrame.

        Args:
        - df (DataFrame): Input DataFrame for analysis.
        """
        self.df = df
        print("The columns are:", df.columns.tolist())

    def bar_chart(self, column):
        """
        Create a bar chart showing the frequency distribution of a column using Seaborn.

        Args:
        - column (str): Column name in the DataFrame.
        """

        # Create the value counts
        value_counts = self.df[column].value_counts()

        plt.figure(figsize=(8, 6))
        sns.barplot(x=value_counts.index, y=value_counts.values, edgecolor="black")

        plt.title(f"Freq Distribution of {column} of heroes")
        plt.xlabel(column)
        plt.ylabel("Frequency")

        plt.xticks(rotation=45)  # Rotate x-axis labels
        plt.tight_layout()
        plt.show()

    def barh_chart(self, column):
        """
        Create a horizontal bar chart showing the frequency distribution of a column using Seaborn.

        Args:
        - column (str): Column name in the DataFrame.
        """
        # Create the value counts
        value_counts = self.df[column].value_counts()

        plt.figure(figsize=(8, 4))
        sns.barplot(x=value_counts.values, y=value_counts.index, edgecolor="black")

        plt.title(f"Freq Distribution of {column} of heroes")
        plt.xlabel("Frequency")
        plt.ylabel(column)

        plt.tight_layout()
        plt.show()

    def hist_chart(self, column, filtered_df=None):
        """
        Create a histogram displaying the distribution of a numerical column using Seaborn.

        Args:
        - column (str): Column name in the DataFrame.
        """
        df = filtered_df
        if filtered_df is None:
            df = self.df
        plt.figure(figsize=(8, 4))
        sns.histplot(data=df, x=column, bins=10, kde=False)

        plt.title(f"Histogram of {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")

        plt.tight_layout()
        plt.show()

    def line_chart(self, column):
        """
        Create a line plot showing the frequency distribution of a column using Seaborn.

        Args:
        - column (str): Column name in the DataFrame.
        """
        value_counts = self.df[column].value_counts().sort_index()

        plt.figure(figsize=(8, 4))
        sns.lineplot(x=value_counts.index, y=value_counts.values, marker="o")

        plt.title(f"Line Plot of {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")

        plt.tight_layout()
        plt.show()

    def boxplot_chart(self, column):
        """
        Create a box plot to visualize the distribution of a column using Seaborn.

        Args:
        - column (str): Column name in the DataFrame.
        """
        plt.figure(figsize=(8, 4))
        sns.boxplot(data=self.df, x=column)

        plt.title(f"Box Plot of {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")

        plt.tight_layout()
        plt.show()

    def get_map(self):
        """
        Fetch the USA state boundaries GeoJSON from Natural Earth.

        Returns:
        - GeoDataFrame: GeoDataFrame containing the USA state boundaries.
        """
        # Fetch the USA state boundaries GeoJSON from Natural Earth
        url = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_1_states_provinces.geojson"
        try:
            response = requests.get(url)
            if response.ok:
                self.usa_map = gpd.read_file(response.text)
            else:
                print("map api fetch failed")
                return
        except HTTPError as e:
            print(f"HTTP error while getting api: {e}")
            return
        except Exception as e:
            print(f"An error occurred while getting api: {e}")
            return

        return self.usa_map

    def GeoName_map(self, column):
        """
        Plot USA States GeoDataFrame using specified column's unique values.

        Args:
        - column (str): Column name in the DataFrame.
        """

        geo_names = self.df[column].unique()
        filtered_usa_map = self.usa_map[self.usa_map["name"].isin(geo_names)]
        unmatched_usa_map = self.usa_map[~self.usa_map["name"].isin(geo_names)]

        _, ax = plt.subplots(1, 1, figsize=(8, 4))
        red_patch = mpatches.Patch(label=column)
        grey_patch = mpatches.Patch(color="lightgrey", label="Unmatched States")
        if len(unmatched_usa_map):
            unmatched_usa_map.plot(color="lightgrey", edgecolor="black", ax=ax)
        filtered_usa_map.plot(edgecolor="black", ax=ax)
        plt.title(f"USA States in {column}")
        plt.legend(handles=[red_patch, grey_patch])
        plt.axis("off")
        plt.show()

    def line_top5gdp(self):
        """
        Plot GDP trends for the top 5 states from the DataFrame.

        Returns:
        - DataFrame: Data filtered for the top 5 states by GDP.
        """
        agg_gdp = self.df.groupby("GeoName")["GDP"].sum().sort_values(ascending=False)

        top_5_states = agg_gdp.head(5).index

        plt.figure(figsize=(12, 8))

        # Filter data for top 5 states
        top_5_data = self.df[self.df["GeoName"].isin(top_5_states)]

        # Plot using Seaborn
        sns.lineplot(data=top_5_data, x="Year", y="GDP", hue="GeoName", marker="o")

        plt.title("GDP Trends for Top 5 States (2017-2022)")
        plt.xlabel("Year")
        plt.ylabel("GDP")
        plt.legend(title="State", loc="upper left")
        plt.grid(True)
        plt.show()
