
import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
SERPAPI_URL = "https://serpapi.com/search.json"

EXCLUDED_SITES = [
    "linkedin.com",
    "naukri.com",
    "indeed.com"
]

JOB_PORTALS = [
    "shine.com",
    "linkedin.com",
    "naukri.com",
    "indeed.com",
    "foundit.in",
    "monster.com",
    "glassdoor.com",
    "timesjobs.com",
    "freshersworld.com",
    "cutshort.io",
    "wellfound.com",
    "hirist.tech",
    "instahyre.com",
    "apna.co"
]


def get_domain(url):
    domain = urlparse(url).netloc.lower()
    return domain.removeprefix("www.")


def is_excluded_site(url):
    domain = get_domain(url)

    return any(
        domain == site or domain.endswith("." + site)
        for site in EXCLUDED_SITES
    )


def get_application_source(url, option_title=""):

    if not url:
        return {
            "apply_type": "not_available",
            "apply_source": "Not Available"
        }

    domain = get_domain(url)

    for portal in JOB_PORTALS:
        if domain == portal or domain.endswith("." + portal):
            return {
                "apply_type": "job_portal",
                "apply_source": option_title or portal
            }

    return {
        "apply_type": "external_site",
        "apply_source": option_title or domain
    }


def create_search_queries(skills, recommended_jobs, experience):

    queries = []

    level = "fresher entry level" if experience == 0 else "entry level"

    # Recommended job titles
    if isinstance(recommended_jobs, list):

        for job in recommended_jobs:

            if isinstance(job, dict):
                title = job.get("title", "")
            elif isinstance(job, str):
                title = job
            else:
                continue

            if title.strip():
                queries.append(
                    f"{title} {level} jobs India"
                )

    # Resume skills: use different combinations
    clean_skills = [
        str(skill).strip()
        for skill in skills
        if str(skill).strip()
    ]

    for skill in clean_skills:
        queries.append(
            f"{skill} developer {level} jobs India"
        )

    # Combined skills
    if len(clean_skills) >= 2:
        queries.append(
            f"{clean_skills[0]} {clean_skills[1]} developer jobs India"
        )

    if not queries:
        queries.append("Python developer fresher jobs India")

    # Remove duplicate queries
    unique_queries = list(dict.fromkeys(queries))

    return unique_queries[:8]


def search_company_jobs(
    skills,
    experience=0,
    location="India",
    recommended_jobs=None
):

    if not SERPAPI_KEY:
        print("Error: SERPAPI_KEY not found in .env")
        return []

    if not isinstance(skills, list):
        skills = []

    if not isinstance(recommended_jobs, list):
        recommended_jobs = []

    all_jobs = []
    seen_jobs = set()
    company_count = {}

    search_queries = create_search_queries(
        skills,
        recommended_jobs,
        experience
    )

    for query in search_queries:

        params = {
            "engine": "google_jobs",
            "q": query,
            "location": location,
            "gl": "in",
            "hl": "en",
            "api_key": SERPAPI_KEY
        }

        try:
            response = requests.get(
                SERPAPI_URL,
                params=params,
                timeout=30
            )

            response.raise_for_status()
            data = response.json()

            if data.get("error"):
                print("SerpApi Error:", data["error"])
                continue

            jobs = data.get("jobs_results", [])

            for item in jobs:

                title = item.get("title", "").strip()
                company = item.get("company_name", "").strip()
                job_location = item.get(
                    "location", "Not specified"
                ).strip()

                description = item.get("description", "")

                if not title or not company:
                    continue

                # Duplicate job check
                job_id = (
                    company.lower() + "|" +
                    title.lower() + "|" +
                    job_location.lower()
                )

                if job_id in seen_jobs:
                    continue

                # Maximum 2 jobs from one company
                company_key = company.lower()

                if company_count.get(company_key, 0) >= 2:
                    continue

                # Find application link
                apply_url = ""
                apply_option_title = ""

                apply_options = item.get("apply_options", [])

                for option in apply_options:

                    link = option.get("link", "")

                    if not link or is_excluded_site(link):
                        continue

                    apply_url = link
                    apply_option_title = option.get("title", "")
                    break

                application_info = get_application_source(
                    apply_url,
                    apply_option_title
                )

                job_text = (
                    title + " " + description
                ).lower()

                matched_skills = [
                    str(skill)
                    for skill in skills
                    if str(skill).lower() in job_text
                ]

                all_jobs.append({

                    "job_id": job_id,

                    "company_name": company,

                    "job_title": title,

                    "location": job_location,

                    "experience_required": "Check job description",

                    "matching_skills": matched_skills,

                    "description": description[:2000],

                    "posted_at": item.get(
                        "detected_extensions", {}
                    ).get("posted_at", "Not specified"),

                    "apply_url": apply_url,

                    "apply_type": application_info["apply_type"],

                    "apply_source": application_info["apply_source"],

                    "job_url": item.get("share_link", ""),

                    "source": "Google Jobs via SerpApi",

                    "listing_found": True

                })

                seen_jobs.add(job_id)

                company_count[company_key] = (
                    company_count.get(company_key, 0) + 1
                )

                if len(all_jobs) >= 30:
                    return all_jobs

        except requests.RequestException as error:
            print("Job Search Error:", error)

        except ValueError as error:
            print("Invalid API Response:", error)

    return all_jobs
