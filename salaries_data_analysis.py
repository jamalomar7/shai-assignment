# -*- coding: utf-8 -*-
"""salaries-data-analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kUuSF1fWWczsSFXY3cYMTjYA2PpWamZu

# Tasks

1. **Basic Data Exploration**: Identify the number of rows and columns in the dataset, determine the data types of each column, and check for missing values in each column.

2. **Descriptive Statistics**: Calculate basic statistics mean, median, mode, minimum, and maximum salary, determine the range of salaries, and find the standard deviation.

3. **Data Cleaning**: Handle missing data by suitable method with explain why you use it.

4. **Basic Data Visualization**: Create histograms or bar charts to visualize the distribution of salaries, and use pie charts to represent the proportion of employees in different departments.

5. **Grouped Analysis**: Group the data by one or more columns and calculate summary statistics for each group, and compare the average salaries across different groups.

6. **Simple Correlation Analysis**: Identify any correlation between salary and another numerical column, and plot a scatter plot to visualize the relationship.

8. **Summary of Insights**: Write a brief report summarizing the findings and insights from the analyses.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
pd.set_option('display.float_format', '{:.2f}'.format)

df = pd.read_csv('/content/Salaries.csv')
df

"""   <table>
        <tr>
            <th>Column Name</th>
            <th>Description</th>
        </tr>
        <tr>
            <td>Id</td>
            <td>Unique identifier for each record</td>
        </tr>
        <tr>
            <td>EmployeeName</td>
            <td>Name of the employee</td>
        </tr>
        <tr>
            <td>JobTitle</td>
            <td>Job title of the employee</td>
        </tr>
        <tr>
            <td>BasePay</td>
            <td>Base salary of the employee</td>
        </tr>
        <tr>
            <td>OvertimePay</td>
            <td>Amount of overtime pay for the employee</td>
        </tr>
        <tr>
            <td>OtherPay</td>
            <td>Other forms of compensation for the employee</td>
        </tr>
        <tr>
            <td>Benefits</td>
            <td>Employee benefits</td>
        </tr>
        <tr>
            <td>TotalPay</td>
            <td>Total pay (Salary) received by the employee</td>
        </tr>
        <tr>
            <td>TotalPayBenefits</td>
            <td>Total pay including benefits</td>
        </tr>
        <tr>
            <td>Year</td>
            <td>Year of the record</td>
        </tr>
        <tr>
            <td>Notes</td>
            <td>Additional notes or comments</td>
        </tr>
        <tr>
            <td>Agency</td>
            <td>Agency or organization name</td>
        </tr>
        <tr>
            <td>Status</td>
            <td>Employee status</td>
        </tr>
    </table>


"""

df.drop(columns=['Id','EmployeeName'], inplace=True)
df

df.nunique()

"""> It looks like **'Status'** and **'Notes'** columns are empty and **'Agency'** has only one value **'San Francisco'**"""

df.drop(columns=[ 'Notes','Status','Agency'], inplace=True)
df

df.dtypes

df.isna().sum()

totalpay_stats = df[['TotalPay']].describe()
stats = pd.DataFrame({'TotalPay': [df['TotalPay'].mode()[0],df['TotalPay'].median()]},
                     index=['mode','median'])

totalpay_stats = pd.concat([totalpay_stats, stats])
totalpay_stats.to_csv('TotalPay_stats.csv')
totalpay_stats

"""> Salaries range from -618 to 567595.43 and 0 is the most requent"""

# Create a 1x3 subplot
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('TotalPay Distribution', fontsize=16)
# Plot Density Plot
axes[0].set_title('Density Plot')
sns.kdeplot(df['TotalPay'], fill=True , ax=axes[0],common_norm=False)
axes[0].tick_params(axis='x', labelrotation=90)

# Plot Histogram
axes[1].set_title('Histogram')
values, edges, patches = axes[1].hist(df['TotalPay'], bins=20, edgecolor='k')

bins = []
for i in range(len(edges) - 1):
        bin_start = edges[i]
        bin_end = edges[i + 1]

        bins.append(bin_start)
        bins.append(bin_end)
        bin_center = (bin_start + bin_end) / 2
        freq = values[i]
        if int(freq) > 0.15 * axes[1].get_ylim()[1]:
            axes[1].text(bin_center, freq / 2, str(int(freq)),
                    ha='center', va='center', color='white', fontsize=10, rotation = 90)
        else:
            axes[1].text(bin_center, freq + 0.01 * axes[1].get_ylim()[1] , str(int(freq)),
                    ha='center', va='bottom', fontsize=10, rotation = 90)

axes[1].set_xticks(bins)
axes[1].tick_params(axis='x', labelrotation=90)
axes[1].set_xlabel('TotalPay')
axes[1].set_ylabel('Count')

# Plot Histogram with KDE Curve
axes[2].set_title('Histogram with KDE Curve')
sns.histplot(df['TotalPay'], bins=20, kde=True, edgecolor='white', ax=axes[2], line_kws={"linewidth": 1})
axes[2].tick_params(axis='x', labelrotation=90)

plt.tight_layout()
plt.savefig('TotalPay_dist.png', dpi=900)
plt.show()

"""> The distribution of **'TotalPay'** is left skewed, a very samll no. of employees get payed more than 200,000"""

df.columns

df_year_grouped = df.groupby(['Year']).agg({

    'TotalPay': ['sum','min', 'max', 'mean', 'std', ('mode', lambda x: x.mode()[0]), ('median',lambda x: x.median() )]
}).reset_index()
df_year_grouped.to_csv('totalpay_stats_yearly.csv')
df_year_grouped

"""> In 2013 the company payed the highest amount of salaries

> In 2014 there was employees who had debts to the company
"""

df_year_title_grouped = df.groupby(['JobTitle','Year']).agg({

    'TotalPay': ['sum','min', 'max', 'mean', 'std', ('mode', lambda x: x.mode()[0]), ('median',lambda x: x.median() )]
}).reset_index()
df_year_title_grouped.to_csv('totalpay_of_each_title_yearly.csv')

sns.heatmap(df.select_dtypes(include='number').corr(), cmap='Reds',annot=True, fmt=".2f", linewidths=.5)
plt.title('Correlation Heatmap')
plt.tight_layout()
plt.savefig('corr_heatmap.png', dpi=900)
plt.show()