import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_md")

skills_list = [
    "python",
    "machine learning",
    "deep learning",
    "data analysis",
    "sql",
    "aws",
    "docker",
    "kubernetes",
    "react",
    "node",
    "mongodb",
    "java",
    "spring boot"
]

def extract_skills(text):
    doc = nlp(text.lower())
    
    matcher = PhraseMatcher(nlp.vocab)
    patterns = [nlp(skill) for skill in skills_list]
    matcher.add("SKILLS", patterns)
    
    matches = matcher(doc)
    
    found_skills = list(set([doc[start:end].text for match_id, start, end in matches]))
    
    return found_skills