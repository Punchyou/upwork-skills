import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.corpus import stopwordsr

nltk.download("stopwords")


# Helper function to clean and preprocess job descriptions
def clean_text(text):
    text = re.sub(r"\s+", " ", text)  # Remove multiple spaces
    text = re.sub(
        r"[^A-Za-z\s]", "", text.lower()
    )  # Remove non-letter characters
    return text


# Function to scrape job descriptions from Upwork (example, replace with API or correct scraping method)
def get_job_descriptions(search_term, num_jobs=10):
    base_url = (
        f"https://www.upwork.com/search/jobs/?q={search_term}&sort=recency"
    )
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = soup.find_all("section", {"data-job-tile": True})[:num_jobs]
    descriptions = []
    for job in jobs:
        description = job.find("span", {"itemprop": "description"})
        if description:
            descriptions.append(clean_text(description.text))

    return descriptions


# Function to extract and rank the most common skills from job descriptions
def extract_common_skills(job_descriptions, top_n=10):
    stop_words = set(stopwords.words("english"))
    vectorizer = CountVectorizer(stop_words=stop_words)

    # Create a document-term matrix
    dt_matrix = vectorizer.fit_transform(job_descriptions)

    # Sum up the counts of each term across all job descriptions
    term_frequencies = dt_matrix.sum(axis=0).A1
    terms = vectorizer.get_feature_names_out()

    # Create a dictionary of terms and their frequencies
    term_freq_dict = dict(zip(terms, term_frequencies))

    # Sort the terms by frequency in descending order
    sorted_terms = sorted(
        term_freq_dict.items(), key=lambda x: x[1], reverse=True
    )

    return sorted_terms[:top_n]


# Main function
def main():
    search_term = "machine learning engineer"  # Customize the search term
    num_jobs = 10  # Number of jobs to scrape and analyze
    top_n = 15  # Number of top skills to display

    job_descriptions = get_job_descriptions(search_term, num_jobs=num_jobs)
    if not job_descriptions:
        print("No job descriptions found.")
        return

    # Extract and display the top skills
    top_skills = extract_common_skills(job_descriptions, top_n=top_n)
    print(f"Top {top_n} most common skills in job postings:")
    for skill, freq in top_skills:
        print(f"{skill}: {freq}")


if __name__ == "__main__":
    main()
