import fitz
import re
import spacy
import pandas as pd
import importlib.util
import subprocess
import os

# ========== Safe spaCy Loader ==========
def get_nlp():
    model_name = "en_core_web_sm"
    try:
        return spacy.load(model_name)
    except OSError:
        subprocess.run(["python", "-m", "spacy", "download", model_name])
        return spacy.load(model_name)

# ========== PDF Text Extraction ==========
def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text

# ========== Entity Extractors ==========
def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else None

def extract_phone(text):
    match = re.search(r'(?:\+91|91|\+91\-)?[\s\-]?[6-9]\d{9}', text)
    return match.group(0).replace(" ", "") if match else None

def extract_skills(text, skill_list):
    text = text.lower()
    return list({skill for skill in skill_list if skill.lower() in text})

def extract_name(text):
    lines = text.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line and "email" not in line.lower() and '@' not in line and len(line.split()) <= 4:
            return line.strip()

    nlp = get_nlp()
    doc = nlp(text[:300])
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text.strip()
    return None

# ========== Master Parser ==========
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
