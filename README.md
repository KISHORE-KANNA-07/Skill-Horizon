# 🚀 Skill-Horizon – AI-Powered Job Recommendation System

Skill-Horizon is a smart, resume-driven job recommendation system built using cutting-edge **Natural Language Processing (NLP)** and **machine learning algorithms**. It allows users to upload a resume, analyzes its content, and recommends the most relevant jobs from a curated dataset.

Whether you're a fresher or an experienced professional, Skill-Horizon helps you expand your potential to new horizons — intelligently and instantly.

---

## 📌 Features

- 📄 **Drag-and-drop resume upload**
- ✨ **Real-time resume parsing** – extract Name, Email, Phone, and Skills
- 🧠 **Semantic matching** of resume skills to job descriptions using:
  - TF-IDF (Text Vectorization)
  - Cosine Similarity
- 📊 **Score bar** and top-match display
- 🌓 **Dark/Light theme toggle**
- ✅ Clean UI with responsive design using Streamlit
- 🔐 **Privacy-friendly** – all processing is done locally

---

## 🧠 Algorithms Used

### 🔍 Resume Parsing
- **Text Extraction**: PyMuPDF (fitz) extracts raw text from PDF.
- **NLP Model**: `spaCy (en_core_web_sm)` is used to extract entities like `PERSON`, and to tokenize content.
- **Regex Matching**: For email and phone number extraction.

### 🤖 Job Matching
- **TF-IDF Vectorization**: Transforms job descriptions and resume content into a numerical vector representation.
- **Cosine Similarity**: Measures the angle between two vectors — higher similarity → better match.

---

## 🏗 Architecture

        +------------------+
        |   User Uploads   |
        |    Resume (PDF)  |
        +--------+---------+
                 |
                 v
     +-----------+------------+
     | Resume Parser Module   |
     | (spaCy, regex, fitz)   |
     +-----------+------------+
                 |
                 v
     +-----------+------------+
     |  Matcher Engine         |
     |  (TF-IDF + Cosine Sim) |
     +-----------+------------+
                 |
                 v
     +-----------+------------+
     |  UI (Streamlit Frontend)|
     +-------------------------+

---

## 📂 Project Structure

Skill-Horizon/
│
├── app.py # Main Streamlit app
├── requirements.txt
├── README.md
│
├── data/
│ ├── skills.csv # List of recognized skills
│ └── full_it_job_dataset.csv # Job dataset
│
├── resume_parser/
│ └── parser.py # PDF & resume extraction logic
│
├── job_dataset/
│ └── processor.py # Preprocessing & vectorization
│
├── recommender/
│ └── matcher.py # Matching logic using cosine similarity
│
├── asserts/
│ └── logo.png # App logo
└── .gitignore

---

## 🧪 Dataset Details

- `skills.csv`: Contains common technical skills (Python, SQL, Java, etc.)
- `full_it_job_dataset.csv`: Job dataset with job titles, descriptions, and skill requirements (can be expanded)

You can swap these with your own job listings or fetch them dynamically from an API.

---

## 🚀 How to Run Locally

### ✅ Prerequisites

- Python 3.8–3.11 recommended
- Install `spaCy` and its English model
- Optional: Create a virtual environment

### 🔧 Installation

```bash
# Clone repo
git clone https://github.com/KISHORE-KANNA-07/Skill-Horizon.git
cd Skill-Horizon

# Setup virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Install spaCy model manually
python -m spacy download en_core_web_sm

# Run the app
streamlit run app.py

#### 🌐 Deployment
Skill-Horizon is deployed on Streamlit Cloud for easy access:
🔗 https://skill-horizon.streamlit.app

#####🧾 Sample Output
Resume parsed successfully

Minimum Match Score input slider

Top matching jobs with:

--Job Title

--Matching Score

--"Show Job Description" toggle

## 🛠 Tech Stack

| Tool            | Purpose                    |
| --------------- | -------------------------- |
| Streamlit       | Frontend Web Interface     |
| spaCy           | NLP Entity Extraction      |
| scikit-learn    | TF-IDF & Cosine Similarity |
| PyMuPDF         | PDF Parsing                |
| pandas/numpy    | Data Preprocessing         |
| GitHub          | Version Control            |
| Streamlit Cloud | App Deployment             |

📋 To-Do (Planned Enhancements)

 Add user login and history tracking

 Resume PDF to preview

 Support for DOCX format

 Real-time API fetching of jobs (e.g., LinkedIn/Indeed scraping)

👨‍💻 Author
Kishore Kanna
🎓 Student | 💼 CSE - AIML | 🎯 Passionate about AI Projects
🔗 [GitHub](https://github.com/KISHORE-KANNA-07/Skill-Horizon)

## 📜 License

Licensed under the MIT License. See `[LICENSE](LICENSE)` for details.