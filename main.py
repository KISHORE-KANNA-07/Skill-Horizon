from resume_parser.parser import parse_resume
from job_dataset.processor import load_and_process_job_data
from recommender.matcher import match_resume_to_jobs

# ====== Step B: Parse Resume ======
resume_path = "C:/Users/kisho/Desktop/job recommendation system/resumes/sample_resume.pdf"
skills_path = "C:/Users/kisho/Desktop/job recommendation system/data/skills.csv"

parsed_resume = parse_resume(resume_path, skills_path)

if parsed_resume:
    print("\n✅ Resume Parsed Successfully!")
    print(f"Name: {parsed_resume['name']}")
    print(f"Email: {parsed_resume['email']}")
    print(f"Phone: {parsed_resume['phone']}")
    print(f"Skills: {parsed_resume['skills']}")
else:
    print("❌ Failed to parse resume.")
    exit()

# ====== Step C & D: Load, Clean, and Vectorize Job Dataset ======
job_data_path = "C:/Users/kisho/Desktop/job recommendation system/data/full_it_job_dataset.csv"
df, tfidf_matrix, vectorizer, kmeans = load_and_process_job_data(job_data_path)

print("\n✅ Job Dataset Loaded and Preprocessed!")
print(f"Total Jobs: {len(df)}")
print(f"TF-IDF Vector Shape: {tfidf_matrix.shape}")

print("\n📦 Job Role Clusters:")
for cluster_num in sorted(df["cluster"].unique()):
    sample_title = df[df["cluster"] == cluster_num]["title"].values[0]
    print(f"→ Cluster {cluster_num}: e.g., {sample_title}")

print("\n🧪 Sample Job Titles:")
for title in df["title"].head(5):
    print(f"→ {title}")

# ====== Step E & F3: Match Resume to Clustered Jobs ======
print("\n🔍 Matching Resume to Job Roles (within Cluster)...")
top_matches, cluster_label = match_resume_to_jobs(
    parsed_resume["skills"],
    df,
    tfidf_matrix,
    vectorizer,
    kmeans,
    top_n=5
)

print(f"\n📦 Predicted Cluster: {cluster_label}")
print("\n🎯 Top Matching Jobs:")
for title, score in top_matches:
    print(f"→ {title} (Match Score: {score}%)")

