from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def normalize_text(s: str) -> str:
    s = s.lower()
    s = re.sub(r'[^a-z0-9\s]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def simple_skill_tokens(skills: List[str]) -> List[str]:
    return [normalize_text(s) for s in skills]

def compute_job_match(profile_text: str, resume_text: str, candidate_skills: List[str], job_text: str, job_skills: List[str]) -> Dict:
    """
    Returns:
      {
        "match_score": 87.0,
        "matching_skills": [...],
        "missing_skills": [...],
        "tfidf_similarity": 0.72,
        "skill_coverage": 0.8,
        "explain": {...}
      }
    """
    # Prepare corpus
    profile_text = normalize_text(profile_text or "")
    resume_text = normalize_text(resume_text or "")
    job_text = normalize_text(job_text or "")
    candidate_skills_norm = simple_skill_tokens(candidate_skills or [])
    job_skills_norm = simple_skill_tokens(job_skills or [])

    # TF-IDF similarity
    corpus = [profile_text + " " + resume_text, job_text]
    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
    tfidf = vectorizer.fit_transform(corpus)
    sim = float(cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0])

    # Skill coverage
    matching_skills = []
    missing_skills = []
    candidate_set = set(candidate_skills_norm)
    job_set = set(job_skills_norm)
    for js in job_set:
        if js in candidate_set:
            matching_skills.append(js)
        else:
            missing_skills.append(js)
    skill_coverage = len(matching_skills) / (len(job_set) if job_set else 1)

    # Weighted score: 60% skill_coverage, 40% tfidf sim
    match_score = (0.6 * skill_coverage + 0.4 * sim) * 100

    return {
        "match_score": round(match_score, 1),
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "tfidf_similarity": round(sim, 3),
        "skill_coverage": round(skill_coverage, 3),
        "explain": {
            "weights": {"skill_coverage": 0.6, "tfidf_similarity": 0.4},
            "skills_considered": list(job_set)
        }
    }
