from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_match_percentage(resume_text, job_description):

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([resume_text, job_description])

    similarity = cosine_similarity(vectors)[0][1]

    return similarity * 100


def skill_match_score(resume_skills, jd_skills):

    if len(jd_skills) == 0:
        return 0

    matched = set(resume_skills).intersection(set(jd_skills))

    return (len(matched) / len(jd_skills)) * 100


def final_score(similarity_score, skill_score):

    score = (0.6 * similarity_score) + (0.4 * skill_score)

    return score
