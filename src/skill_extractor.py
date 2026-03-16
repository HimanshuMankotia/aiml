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

    text = text.lower()

    found_skills = []

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))
