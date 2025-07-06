import fitz
import re
import spacy
import pandas as pd

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text

def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else None

def extract_phone(text):
    match = re.search(r'(?:\+91|91|\+91\-)?[\s\-]?[6-9]\d{9}', text)
    return match.group(0).replace(" ", "") if match else None

def extract_skills(text, skill_list):
    found = []
    text = text.lower()
    for skill in skill_list:
        if skill.lower() in text:
            found.append(skill)
    return list(set(found))

def extract_name(text):
    # Try grabbing the first line if it's a name
    lines = text.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line and "email" not in line.lower() and '@' not in line and len(line.split()) <= 4:
            return line.strip()

    # If that fails, fallback to spaCy
    doc = nlp(text[:300])
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text.strip()

    return None


def parse_resume(pdf_path, skills_path="data/skills.csv"):
    text = extract_text_from_pdf(pdf_path)
    skill_df = pd.read_csv(skills_path)
    skill_list = skill_df['skill'].tolist()

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text, skill_list),
        "raw_text": text
    }
