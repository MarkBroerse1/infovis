import csv
import plotly.express as px
from collections import defaultdict
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np








def get_happiness_scores_by_continent(filename):
    import csv
    import plotly.express as px

    continent_scores = {}

    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            continent = row['continent']
            year = int(row['Year'])
            happiness_score = round(float(row['happiness_score']))
            education_index = min(float(row['Education_Index']) * 10, 10)
            education_index = round(education_index) / 10
            gni_per_capita = float(row['GNI_per_capita_PPP']) if row['GNI_per_capita_PPP'] != '' else 0
            gni_per_capita = int(gni_per_capita) // 10000 * 10000
            life_expectancy_index = min(float(row['life_expectancy_index']) * 10, 10)
            life_expectancy_index = round(life_expectancy_index) / 10

            if continent not in continent_scores:
                continent_scores[continent] = {'Year': [], 'Happiness Score': [], 'Education Index': [], 'GNI per capita': [], 'Life Expectancy Index': []}
            continent_scores[continent]['Year'].append(year)
            continent_scores[continent]['Education Index'].append(education_index)
            continent_scores[continent]['Happiness Score'].append(happiness_score)
            continent_scores[continent]['GNI per capita'].append(gni_per_capita)
            continent_scores[continent]['Life Expectancy Index'].append(life_expectancy_index)

    data = []
    for continent, scores in continent_scores.items():
        sorted_scores = sorted(zip(scores['Year'], scores['Education Index'], scores['GNI per capita'], scores['Happiness Score'], scores['Life Expectancy Index']), key=lambda x: (x[1], -x[2], -x[3]))
        data.extend([
            {'Continent': continent, 'Education Index': education_index, 'Year': year, 'GNI per capita': gni_per_capita, 'Happiness Score': score, 'Life Expectancy Index': life_expectancy_index}
            for year, education_index, gni_per_capita, score, life_expectancy_index in sorted_scores
        ])

    # Sort the rest of the categories
    for category in ['Year', 'GNI per capita', 'Happiness Score', 'Life Expectancy Index']:
        data = sorted(data, key=lambda x: x[category])

    dimensions_order = ['Continent', 'Year', 'Education Index', 'GNI per capita', 'Happiness Score', 'Life Expectancy Index']
    dimensions_labels = {'Happiness Score': 'Happiness Score'}

    fig = px.parallel_categories(data, dimensions=dimensions_order, color='Happiness Score', color_continuous_scale='Viridis',
                                 labels=dimensions_labels)
    fig.show()

# Example usage
get_happiness_scores_by_continent('full_data.csv')



def get_happiness_scores_by_continent2(filename):
    continent_scores = defaultdict(list)

    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            continent = row['continent']
            country = row['Country']
            year = row['Year']
            happiness_score = float(row['happiness_score'])
            continent_scores[continent].append((country, year, happiness_score))

    # Create the seaborn stacked histogram
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 8))

    # Define a color palette for the continents
    palette = sns.color_palette("deep", len(continent_scores))

    # Create a list to store the heights of each country within a continent
    country_heights = []

    for continent, scores in continent_scores.items():
        heights = [score for _, _, score in scores]
        country_heights.append(heights)

    # Plot the stacked histogram
    bars = plt.hist(country_heights, bins=20, stacked=True, label=list(continent_scores.keys()), color=palette, alpha=0.8, linewidth=0)


    # Create the legend
    legend_patches = [mpatches.Patch(color=palette[i], label=continent) for i, continent in enumerate(continent_scores.keys())]
    plt.legend(handles=legend_patches, loc='upper right', fontsize='small')

    # Add hover functionality
    fig = plt.gcf()
    ax = plt.gca()

    def hover(event):
        for container in bars:
            for rect in container:
                cont, ind = rect.contains(event)
                if cont:
                    heights = [height.get_height() for height in container]
                    countries = [country for country in continent_scores.keys()]
                    bins = bars[1]
                    bin_width = np.diff(bins)[0]
                    index = ind["ind"][0]
                    x = bars[1][index] + bin_width / 2
                    y = heights[index]
                    plt.annotate(f"{countries[index]}: {y:.2f}", xy=(x, y), xytext=(x, y + 0.2),
                                 ha='center', va='bottom', color='black', alpha=0.7,
                                 arrowprops=dict(arrowstyle='-', lw=0.5, color='black'))
                    fig.canvas.draw_idle()

    plt.xlabel("Happiness Score")
    plt.ylabel("Count")
    plt.title("Stacked Histogram of Happiness Scores by Continent")
    plt.tight_layout()
    sns.despine()

    plt.show()

# Example usage
get_happiness_scores_by_continent2('full_data.csv')
