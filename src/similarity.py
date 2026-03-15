import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_md")

def semantic_similarity(resume_text, job_description):
    resume_doc = nlp(resume_text)
    jd_doc = nlp(job_description)
    return resume_doc.similarity(jd_doc)

def tfidf_similarity(resume_text, job_description):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, job_description])
    return cosine_similarity(vectors)[0][1]

def calculate_match_percentage(resume_text, job_description):
    semantic_score = semantic_similarity(resume_text, job_description)
    tfidf_score = tfidf_similarity(resume_text, job_description)
    
    final_score = (0.6 * semantic_score) + (0.4 * tfidf_score)
    return final_score * 100

def skill_match_score(resume_skills, jd_skills):
    if len(jd_skills) == 0:
        return 0

    matched = set(resume_skills).intersection(set(jd_skills))
    return len(matched) / len(jd_skills)