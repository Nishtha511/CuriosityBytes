import pandas as pd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import numpy as np

def get_recommendations(user_id, userSearchHistory):
    userSearchHistory['title'] = userSearchHistory['search_query'].str.lower()
    userSearchHistory['user_id'] = userSearchHistory['user_id'].str.lower().apply(email_to_int)
    userSearchHistory['tags'] = userSearchHistory['search_query'].str.lower().apply(get_category)
    userSearchHistory['video_id'] = userSearchHistory['search_query'].factorize()[0]
    video_metadata = userSearchHistory[['video_id', 'title', 'tags']].drop_duplicates()
    userSearchHistory_grouped = userSearchHistory.groupby(['user_id', 'title', 'video_id']).size().reset_index(name='interaction_score')
    print(userSearchHistory_grouped)

    user_history = userSearchHistory_grouped[['user_id', 'video_id', 'interaction_score']]
    print(video_metadata)
    print(user_history)
    user_id = email_to_int(user_id)
    recommendations = hybrid_recommendations(user_id, user_history, video_metadata, top_n=5)
    print("\nRecommended Videos for User {}:\n".format(user_id), recommendations)
    return recommendations


def content_based_recommendations(user_id, user_history, video_metadata, top_n=5):
    
    user_videos = user_history[user_history['user_id'] == user_id]
    user_videos = user_videos.merge(video_metadata, on='video_id', how='inner')
    
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(video_metadata['tags'])
    
    user_video_ids = user_videos['video_id'].tolist()    
    video_id_to_index = {video_id: idx for idx, video_id in enumerate(video_metadata['video_id'])}
    user_video_indices = [video_id_to_index[vid] for vid in user_video_ids if vid in video_id_to_index]
    
    content_similarities = cosine_similarity(tfidf_matrix)
    candidate_videos = video_metadata[~video_metadata['video_id'].isin(user_video_ids)]
    avg_similarity_scores = content_similarities[user_video_indices].mean(axis=0)
    recommended_indices = avg_similarity_scores.argsort()[-top_n:][::-1]

    return video_metadata.iloc[recommended_indices][['video_id', 'title']]


def collaborative_recommendations(user_id, user_history, video_metadata, top_n):
    user_item_matrix = pd.pivot_table(user_history, index='user_id', columns='video_id', values='interaction_score', fill_value=0)
    
    model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=top_n+1)
    model_knn.fit(user_item_matrix.values.T)
    
    user_index = user_item_matrix.index.get_loc(user_id)
    distances, indices = model_knn.kneighbors(user_item_matrix.values.T[user_index].reshape(1, -1), n_neighbors=top_n+1)
    
    similar_users = indices.flatten()[1:]
    recommended_video_ids = []
    
    for sim_user in similar_users:
        if sim_user >= 0 and sim_user < user_item_matrix.shape[0]:
            sim_user_videos = user_item_matrix.iloc[sim_user].values
            sim_user_videos_indices = np.nonzero(sim_user_videos)[0]
            recommended_video_ids.extend(user_item_matrix.columns[sim_user_videos_indices])
        else:
            print(f"Skipping out-of-bounds similar user index: {sim_user}")
    
    user_video_ids = user_item_matrix.loc[user_id].values
    user_video_ids_indices = np.nonzero(user_video_ids)[0]
    user_video_ids = user_item_matrix.columns[user_video_ids_indices].tolist()
    
    recommended_video_ids = [vid for vid in recommended_video_ids if vid not in user_video_ids]    
    recommended_video_ids = list(set(recommended_video_ids))[:top_n]
    recommended_videos = video_metadata[video_metadata['video_id'].isin(recommended_video_ids)]
    
    return recommended_videos[['video_id', 'title']]


def hybrid_recommendations(user_id, user_history, video_metadata, top_n=5):
    content_recs = content_based_recommendations(user_id, user_history, video_metadata, top_n)
    collaborative_recs = collaborative_recommendations(user_id, user_history, video_metadata, top_n)
    
    combined_recs = pd.concat([content_recs, collaborative_recs]).drop_duplicates().head(top_n)
    return combined_recs


base_url = "https://api.datamuse.com/words"
def get_category(line):
    params = {
        "ml": line,
        "max": 1
    }
    response = requests.get(base_url, params=params)
    return response.json()[0]["word"]


def email_to_int(email):
    return abs(hash(email)) % (10 ** 8)