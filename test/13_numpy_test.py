import pandas as pd
import numpy as np
import os

movies = pd.read_csv("http://bit.ly/imdbratings")

first_10_rows = movies.head(10)
last_10_rows = movies.tail(10)

tuple = movies.shape
columns = movies.columns

duration_gt_200 = movies[movies.duration >= 200]
duration_gt_200_and_genre_crime = movies[
    (movies.duration >= 200) & (movies.genre == "Crime")
]

like_movies = movies[movies.genre.isin(["Crime", "Drama"])]

categories = movies["genre"].unique()

categories_2 = movies.genre.map(
    {
        "Crime": "Adult",
        "Horror": "Adult",
        "Comedy": "Kids",
    }
)
