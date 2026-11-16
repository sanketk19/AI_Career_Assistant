
import os
from google import genai
from dotenv import load_dotenv
from google.genai import types

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# AI Chatbot Response with Conversation Memory
def generate_gemini_response(
    prompt,
    candidate_info=None,
    career_roadmap=None,
    chat_history=None
):
    try:
        chat_history = chat_history or []

        conversation = ""

        for chat in chat_history[-10:]:
            role = chat.get("role", "user")
            message = chat.get("text", "")

            if role in ["user", "assistant"] and message:
                speaker = (
                    "User" if role == "user"
                    else "AI Assistant"
                )

                conversation += f"{speaker}: {message}\n"

        instruction = f"""
You are a professional AI Career Assistant.

STRICT ANSWER FORMATTING RULES:

1. Always answer in numbered points.
2. Never write long paragraphs.
3. Each point must be on a separate line.
4. Keep each point short and simple.
5. Use simple English.
6. Give maximum 6 to 8 points.
7. Use headings when necessary.
8. Do not combine multiple points into one paragraph.
9. Use bullet points under a heading if needed.
10. Keep answers professional and easy to understand.
11. Avoid unnecessary introductions and conclusions.
12. Give direct answers.

EXAMPLE FORMAT:

**1. Current Skills**
- Python
- Django
- React

**2. Skills to Learn**
- Django REST Framework
- Docker
- AWS

**3. Learning Plan**
- First learn Django REST Framework.
- Then practice API development.

CANDIDATE RESUME INFORMATION:
{candidate_info if candidate_info else "Resume not uploaded."}

CAREER ROADMAP:
{career_roadmap if career_roadmap else "Career roadmap not generated yet."}

PREVIOUS CONVERSATION:
{conversation if conversation else "No previous conversation."}

CURRENT USER QUESTION:
{prompt}

IMPORTANT:
Return the answer in separate numbered points.
Do not write a long paragraph.
Do not invent candidate skills or experience.
Use previous conversation when answering follow-up questions.
"""

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=instruction
        )

        return response.text

    except Exception as e:
        return f"Gemini API Error: {str(e)}"


# AI Resume Analysis and Experience Detection
def analyze_resume(resume_text):
    try:
        prompt = f"""
You are an expert AI Resume Analyzer and Career Advisor.

Analyze the resume carefully.

Return valid JSON only.

Use this exact JSON structure:

{{
    "candidate_type": "Fresher",
    "total_experience_years": 0,
    "internship_experience_months": 0,
    "skills": [
        "Python",
        "Django",
        "React"
    ],
    "education": "MCA",
    "analysis": "Complete resume analysis with headings and bullet points.",
    "recommended_jobs": [
        {{
            "title": "Python Developer",
            "required_skills": [
                "Python",
                "Django",
                "SQL"
            ],
            "experience_required": "0-1 years",
            "match_percentage": 85,
            "reason": "Good match with resume skills"
        }}
    ]
}}

EXPERIENCE DETECTION RULES:
1. Identify whether candidate is Fresher or Experienced.
2. Check professional full-time work experience separately.
3. Do not count academic projects as work experience.
4. Do not count internships as full-time experience.
5. Mention internship duration separately in months.
6. If no professional experience is found, candidate_type must be Fresher.
7. Never assume experience if dates or details are missing.
8. If experience is unclear, mention it in analysis.

JOB RECOMMENDATION RULES:
1. Recommend jobs according to candidate skills and experience.
2. Fresher candidates should receive Fresher, Internship,
   Trainee, Junior and 0-1 year jobs.
3. Experienced candidates should receive jobs suitable
   for their actual experience.
4. Do not recommend jobs requiring more experience
   than the candidate has.
5. Avoid duplicate and irrelevant jobs.
6. Suggest all relevant job roles, not a fixed number of jobs.
7. Match percentage must be between 0 and 100.
8. Never invent candidate skills or experience.

ANALYSIS RULES:
1. Use simple English.
2. Include Candidate Summary.
3. Include Technical Skills.
4. Include Experience.
5. Include Education.
6. Include Suitable Job Roles.
7. Include Missing Skills.
8. Include Resume Score out of 100.
9. Include Improvement Suggestions.
10. If information is missing, mention Not Available.

IMPORTANT:
These are job role recommendations only.
Do not claim that a company has an actual vacancy.
Actual company vacancies will be checked separately.

Return valid JSON only.
Do not use Markdown code blocks.

RESUME CONTENT:
{resume_text[:12000]}
"""

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        return response.text

    except Exception as e:
        raise Exception(
            f"Resume Analysis Error: {str(e)}"
        )


# AI Career Roadmap Generator
def generate_career_roadmap(candidate_info):
    try:
        prompt = f"""
You are a professional AI Career Roadmap Generator.

Create a personalized career roadmap using this candidate information.

Candidate Information:
{candidate_info}

Return valid JSON only with this structure:

{{
    "career_goal": "Python Full Stack Developer",
    "current_level": "Beginner",
    "current_skills": ["Python", "Django"],
    "skills_to_learn": ["REST API", "React", "SQL"],
    "roadmap": [
        {{
            "phase": "Phase 1",
            "title": "Python Fundamentals",
            "duration": "2 Weeks",
            "topics": [
                "Python basics",
                "OOP",
                "Functions"
            ],
            "project": "Build a Python CRUD application"
        }}
    ],
    "recommended_projects": [
        "Student Management System",
        "AI Career Assistant"
    ],
    "estimated_timeline": "3 to 4 Months"
}}

RULES:
1. Use the candidate's actual skills.
2. Do not invent existing skills.
3. Recommend skills required for the career goal.
4. Give a step-by-step learning roadmap.
5. Recommend practical projects.
6. Use simple English.
7. Keep the roadmap suitable for the candidate's experience.
8. Give at least 4 learning phases.
9. Include practical projects in the roadmap.
10. Return valid JSON only without Markdown.
"""

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        return response.text

    except Exception as e:
        raise Exception(
            f"Career Roadmap Error: {str(e)}"
        )
