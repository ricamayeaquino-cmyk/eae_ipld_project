# The libraries you have to use
import pandas as pd
import matplotlib.pyplot as plt

# Some extra libraries to build the webapp
import streamlit as st


# ----- Left menu -----
with st.sidebar:
    st.image("eae_img.png", width=200)
    st.write("Interactive Project to load a dataset with information about Netflix Movies and Series, extract some insights using Pandas and displaying them with Matplotlib.")
    st.write("Data extracted from: https://www.kaggle.com/datasets/shivamb/netflix-shows (with some cleaning and modifications)")


# ----- Title of the page -----
st.title("🎬 Netflix Data Analysis")
st.divider()


# ----- Loading the dataset -----

@st.cache_data
def load_data():
    data_path = "data/netflix_titles.csv"
    movies_df = pd.read_csv(data_path, index_col="show_id")
    return movies_df

movies_df = load_data()

# Displaying the dataset in a expandable table
with st.expander("Check the complete dataset:"):
    st.dataframe(movies_df)


# ----- Extracting some basic information from the dataset -----

# Ex 2.2: What is the min and max release years?
min_year = movies_df['release_year'].min()
max_year = movies_df['release_year'].max()

# Ex 2.3: How many director names are missing values (NaN)?
num_missing_directors = movies_df['director'].isna().sum()

# Ex 2.4: How many different countries are there in the data?
movies_df['country'] = movies_df['country'].fillna("Unknown")
all_countries = ", ".join(movies_df['country'].tolist()).split(", ")
n_countries = len(set(all_countries))

# Ex 2.5: How many characters long are on average the title names?
movies_df['title_length'] = movies_df['title'].apply(lambda x: len(x))
avg_title_length = movies_df['title_length'].mean()


# ----- Displaying the extracted information metrics -----

st.write("##")
st.header("Basic Information")

cols1 = st.columns(5)
cols1[0].metric("Min Release Year", min_year)
cols1[1].metric("Max Release Year", max_year)
cols1[2].metric("Missing Dir. Names", num_missing_directors)
cols1[3].metric("Countries", n_countries)
cols1[4].metric("Avg Title Length", str(round(avg_title_length, 2)) if avg_title_length is not None else None)


# ----- Pie Chart: Top year producer countries -----

st.write("##")
st.header("Top Year Producer Countries")

cols2 = st.columns(2)
year = cols2[0].number_input("Select a year:", min_year, max_year, 2005)

# Ex 2.6: For a given year, get the top 10 countries
year_data = movies_df.loc[movies_df['release_year'] == year, 'country']

# Split countries and count each one individually
country_list = []
for countries in year_data:
    if pd.notna(countries):  # Check if not NaN
        # Split by comma and strip whitespace
        split_countries = [country.strip() for country in countries.split(',')]
        country_list.extend(split_countries)

# Convert to Series and get value counts
country_counts = pd.Series(country_list).value_counts()

# Get top 10 and sort in descending order
top_10_countries = country_counts.head(10).sort_values(ascending=False)

# Netflix red gradient - darkest to lightest
netflix_reds = ['#660708', '#831010', '#9d0208', '#B20710', '#d00000', 
                '#E50914', '#dc2f02', '#e85d04', '#f48c06', '#ffba08']

if top_10_countries is not None and len(top_10_countries) > 0:
    fig = plt.figure(figsize=(8, 8))
    plt.pie(top_10_countries, 
            labels=top_10_countries.index, 
            autopct="%.2f%%",
            startangle=90,      # Start at 0 degrees (12 o'clock)
            counterclock=False, # Go clockwise
            colors=netflix_reds) # Netflix red gradient
    plt.title(f"Top 10 Countries in {year}")

    st.pyplot(fig)
else:
    st.subheader("⚠️ No data available for this year.")


# ----- Line Chart: Avg duration of movies by year -----

st.write("##")
st.header("Avg Duration of Movies by Year")

# Ex 2.7: Make a line chart of the average duration of movies
# Filter only movies (not TV Shows)
movies_only = movies_df[movies_df['type'] == 'Movie'].copy()

# Extract minutes as integers from the duration column
movies_only['duration_minutes'] = movies_only['duration'].apply(
    lambda x: int(x.split()[0]) if pd.notna(x) and 'min' in x else None
)

# Group by year and calculate average duration
movies_avg_duration_per_year = movies_only.groupby('release_year')['duration_minutes'].mean()

if movies_avg_duration_per_year is not None and len(movies_avg_duration_per_year) > 0:
    fig = plt.figure(figsize=(9, 6))
    plt.plot(movies_avg_duration_per_year.index, 
             movies_avg_duration_per_year.values, 
             marker='o', 
             linewidth=2,
             color='#E50914',           # Netflix red
             markerfacecolor='#E50914', # Netflix red markers
             markeredgecolor='#B20710', # Darker red edge
             markersize=6)

    plt.xlabel("Year")
    plt.ylabel("Average Duration (minutes)")
    plt.title("Average Duration of Movies Across Years")
    plt.grid(True, alpha=0.3)
    st.pyplot(fig)
else:
    st.subheader("⚠️ You still need to develop the Ex 2.7.")