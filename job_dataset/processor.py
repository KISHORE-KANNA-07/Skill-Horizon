import pandas as pd
import re
import string
import spacy
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

'''# Load spaCy model and stopwords
nlp = spacy.load("en_core_web_sm")
stop_words = set(stopwords.words("english"))

def load_and_process_job_data(filepath):
    """
    Step C & D: Load the job dataset, clean the skill sets,
    and vectorize them using TF-IDF for further matching.
    """

    # Load the dataset
    df = pd.read_csv(filepath)

    # Drop rows with missing titles or skills
    df.dropna(subset=["job_title", "job_skill_set"], inplace=True)

    # Strip and lowercase the skill set strings
    df["job_title"] = df["job_title"].str.strip()
    df["job_skill_set"] = df["job_skill_set"].str.strip().str.lower()

    # Optional: remove duplicates if any
    df.drop_duplicates(subset=["job_title", "job_skill_set"], inplace=True)

    # TF-IDF Vectorization (Split by comma-separated skills)
    vectorizer = TfidfVectorizer(token_pattern=r"[^,]+")
    tfidf_matrix = vectorizer.fit_transform(df["job_skill_set"])

    return df, tfidf_matrix, vectorizer'''

def load_and_process_job_data(file_path, num_features=5000, num_clusters=6):
    import pandas as pd

    df = pd.read_csv(file_path)

    # Rename for consistency
    df = df.rename(columns={
        "job_title": "title",
        "job_description": "description",
        "job_skill_set": "skills"
    })

    df = df[["title", "skills"]].dropna()

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(max_features=num_features)
    tfidf_matrix = vectorizer.fit_transform(df["skills"])

    # === F3: Clustering ===
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(tfidf_matrix)
    df["cluster"] = cluster_labels

    return df, tfidf_matrix, vectorizer, kmeans
