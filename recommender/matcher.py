from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

'''def match_resume_to_jobs(resume_skills, vectorizer, tfidf_matrix, df, top_n=5, min_score=15.0, filter_keywords=None):
    if not resume_skills:
        return []

    # Resume skills → single text
    boost_keywords = {"python", "machine learning", "sql", "javascript", "react", "java"}
    resume_text = boost_skills(resume_skills, boost_keywords=boost_keywords, boost_factor=3)
    resume_vector = vectorizer.transform([resume_text])
    similarity_scores = cosine_similarity(resume_vector, tfidf_matrix)

    top_indices = np.argsort(similarity_scores[0])[::-1]

    matched_jobs = []
    for idx in top_indices:
        score = round(similarity_scores[0][idx] * 100, 2)

        if score < min_score:
            continue

        job_title = df.iloc[idx]["job_title"]

        if filter_keywords:
            if not any(keyword.lower() in job_title.lower() for keyword in filter_keywords):
                continue

        matched_jobs.append({
            "job_title": job_title,
            "score": score
        })

        if len(matched_jobs) >= top_n:
            break

    return matched_jobs
def boost_skills(skills, boost_keywords=None, boost_factor=3):
    boosted = []
    for skill in skills:
        skill_lower = skill.lower()
        if boost_keywords and skill_lower in boost_keywords:
            boosted.extend([skill_lower] * boost_factor)
        else:
            boosted.append(skill_lower)
    return ", ".join(boosted)'''


def match_resume_to_jobs(resume_skills, df, tfidf_matrix, vectorizer, kmeans_model, top_n=5, min_score=15):
    resume_text = " ".join(resume_skills)
    resume_vector = vectorizer.transform([resume_text])

    # Predict cluster
    cluster_label = kmeans_model.predict(resume_vector)[0]

    # Filter jobs in the same cluster
    cluster_indices = df[df["cluster"] == cluster_label].index
    filtered_matrix = tfidf_matrix[cluster_indices]

    # Cosine similarity
    similarity_scores = cosine_similarity(resume_vector, filtered_matrix).flatten()
    top_indices_within_cluster = similarity_scores.argsort()[::-1][:top_n]
    top_indices = cluster_indices[top_indices_within_cluster]

    top_matches = []
    for i, idx in enumerate(top_indices):
        score = similarity_scores[top_indices_within_cluster[i]]
        score_percentage = round(score * 100, 2)

        if score_percentage < min_score:
            continue

        job = df.iloc[idx]
        top_matches.append({
            "title": job["title"],
            "score": score_percentage,
            "description": job.get("description", "No description available.")
        })

    return top_matches
