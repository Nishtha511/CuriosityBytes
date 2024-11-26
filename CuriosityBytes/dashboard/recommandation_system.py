# Import necessary libraries
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import numpy as np

# Step 1: Load user and video data (assumes CSVs but can replace with database queries)
# Replace these with your actual database calls
user_history = pd.read_csv("user_history.csv")  # User interaction history: user_id, video_id, interaction_score
video_metadata = pd.read_csv("video_metadata.csv")  # Video info: video_id, title, tags, category

# Preview the data
print("User History:\n", user_history.head())
print("Video Metadata:\n", video_metadata.head())

# Step 2: Content-based filtering
def content_based_recommendations(user_id, user_history, video_metadata, top_n=5):
    # Merge user history with video metadata
    user_videos = user_history[user_history['user_id'] == user_id]
    user_videos = user_videos.merge(video_metadata, on='video_id', how='inner')
    
    # Combine tags and category as a single content feature
    video_metadata['content'] = video_metadata['tags'] + " " + video_metadata['category']
    
    # TF-IDF Vectorizer for text similarity
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(video_metadata['content'])
    
    # Get user interaction video IDs and calculate similarity scores
    user_video_ids = user_videos['video_id'].tolist()
    
    # Create a mapping of video_id to its index in the video_metadata DataFrame
    video_id_to_index = {video_id: idx for idx, video_id in enumerate(video_metadata['video_id'])}
    
    # Convert user_video_ids to indices
    user_video_indices = [video_id_to_index[vid] for vid in user_video_ids if vid in video_id_to_index]
    
    content_similarities = cosine_similarity(tfidf_matrix)
    
    # Average content similarity for non-watched videos
    candidate_videos = video_metadata[~video_metadata['video_id'].isin(user_video_ids)]
    
    # Calculate the average similarity for the user’s watched videos
    avg_similarity_scores = content_similarities[user_video_indices].mean(axis=0)
    
    # Get top recommendations based on the average similarity scores
    recommended_indices = avg_similarity_scores.argsort()[-top_n:][::-1]
    
    return video_metadata.iloc[recommended_indices][['video_id', 'title']]




# Step 3: Collaborative filtering

def collaborative_recommendations(user_id, user_history, video_metadata, top_n):
    # Create a user-item interaction matrix (user_id, video_id)
    user_item_matrix = pd.pivot_table(user_history, index='user_id', columns='video_id', values='interaction_score', fill_value=0)
    
    # Train a KNN model on the user-item matrix
    model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=top_n+1)
    model_knn.fit(user_item_matrix.values.T)  # Transpose to make videos as rows
    
    # Find the user index in the user-item matrix
    user_index = user_item_matrix.index.get_loc(user_id)
    
    # Find nearest neighbors (other users similar to the input user)
    distances, indices = model_knn.kneighbors(user_item_matrix.values.T[user_index].reshape(1, -1), n_neighbors=top_n+1)
    
    # Exclude the user themselves
    similar_users = indices.flatten()[1:]  # Exclude the first index (which is the user themselves)
    
    recommended_video_ids = []  # Initialize an empty list
    
    for sim_user in similar_users:
        # Ensure the similar user index is within bounds
        if sim_user >= 0 and sim_user < user_item_matrix.shape[0]:
            # Get watched videos by similar user
            sim_user_videos = user_item_matrix.iloc[sim_user].values  # Convert to NumPy array
            sim_user_videos_indices = np.nonzero(sim_user_videos)[0]  # Find indices of non-zero entries
            recommended_video_ids.extend(user_item_matrix.columns[sim_user_videos_indices])  # Add video IDs
        else:
            print(f"Skipping out-of-bounds similar user index: {sim_user}")
    
    # Get videos already watched by the user
    user_video_ids = user_item_matrix.loc[user_id].values  # Convert to NumPy array
    user_video_ids_indices = np.nonzero(user_video_ids)[0]  # Get the indices of non-zero entries
    user_video_ids = user_item_matrix.columns[user_video_ids_indices].tolist()  # Convert to a list of video IDs
    
    # Filter out videos already watched by the user
    recommended_video_ids = [vid for vid in recommended_video_ids if vid not in user_video_ids]
    
    # Return top_n unique recommended videos as a DataFrame
    recommended_video_ids = list(set(recommended_video_ids))[:top_n]
    recommended_videos = video_metadata[video_metadata['video_id'].isin(recommended_video_ids)]
    
    return recommended_videos[['video_id', 'title']]  # Return relevant columns



# Step 4: Hybrid recommendation system
def hybrid_recommendations(user_id, user_history, video_metadata, top_n=5):
    content_recs = content_based_recommendations(user_id, user_history, video_metadata, top_n)
    collaborative_recs = collaborative_recommendations(user_id, user_history, video_metadata, top_n)
    
    # Combine recommendations with weights (e.g., 70% content, 30% collaborative)
    combined_recs = pd.concat([content_recs, collaborative_recs]).drop_duplicates().head(top_n)
    return combined_recs



user_id = 1  # Replace with your test user ID
recommendations = hybrid_recommendations(user_id, user_history, video_metadata, top_n=5)
print("\nRecommended Videos for User {}:\n".format(user_id), recommendations)



