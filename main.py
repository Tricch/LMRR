import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Read the ratings data from the CSV file
ratings_df = pd.read_csv('ratings.csv')

# Add a row for the new user (user_id 10067)
new_user_data = {'user_id': 10067, 'r_id': 1, 'ratings': 5}
ratings_df.loc[len(ratings_df)] = new_user_data

# Ensure the 'ratings' column is numeric
ratings_df['ratings'] = pd.to_numeric(ratings_df['ratings'])

# Pivot the dataframe to have users as rows and items as columns
pivot_df = ratings_df.pivot_table(index='user_id', columns='r_id', values='ratings', fill_value=0)

# Extract the new user's ratings
new_user_ratings = pivot_df.loc[10067].values.reshape(1, -1)

# Calculate cosine similarity
cosine_sim = cosine_similarity(pivot_df, new_user_ratings)

# Calculate Euclidean distance
euclidean_dist = pivot_df.apply(lambda row: np.linalg.norm(row.values - new_user_ratings), axis=1)

# Combine results into a DataFrame
result_df = pd.DataFrame({'user_id': pivot_df.index, 'cosine_similarity': cosine_sim.flatten(), 'euclidean_distance': euclidean_dist})

# Read user data from the 'auth_user.csv' file
user_data = pd.read_csv('auth_user.csv')

# Reset the index before merging
result_df.reset_index(drop=True, inplace=True)

# Merge with the user data to get usernames
result_df = pd.merge(result_df, user_data, on='user_id')

# Recommend items based on highest cosine similarity or lowest Euclidean distance
top_cosine_recommendations = result_df.sort_values(by='cosine_similarity', ascending=False).head(5)
top_euclidean_recommendations = result_df.sort_values(by='euclidean_distance').head(5)

# Extract the recommended items (r_id) based on ratings
recommended_items_cosine = ratings_df[ratings_df['user_id'].isin(top_cosine_recommendations['user_id'])]['r_id'].unique()
recommended_items_euclidean = ratings_df[ratings_df['user_id'].isin(top_euclidean_recommendations['user_id'])]['r_id'].unique()

print("Top 5 recommendations based on cosine similarity:")
print(top_cosine_recommendations[['user_id', 'username']])
print("Recommended items based on ratings:")
print(recommended_items_cosine)

print("\nTop 5 recommendations based on Euclidean distance:")
print(top_euclidean_recommendations[['user_id', 'username']])
print("Recommended items based on ratings:")
print(recommended_items_euclidean)
