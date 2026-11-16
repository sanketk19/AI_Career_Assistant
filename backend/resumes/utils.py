
import fitz
import re


# PDF मधून संपूर्ण text extract करणे
def extract_text_from_pdf(pdf_file):

    pdf_file.seek(0)

    document = fitz.open(
        stream=pdf_file.read(),
        filetype="pdf"
    )

    extracted_text = ""

    for page in document:
        extracted_text += page.get_text() + "\n"

    document.close()
    pdf_file.seek(0)

    return extracted_text


# Resume मधून सर्व माहिती extract करणे
def extract_resume_details(text):

    # Email extract करणे
    email_match = re.search(
        r'[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}',
        text
    )

    email = email_match.group(0) if email_match else ""

    # Phone number extract करणे
    phone_match = re.search(
        r'(?:\+91[\s-]?)?[6-9]\d{9}',
        text
    )

    phone = phone_match.group(0) if phone_match else ""

    # Candidate Name extract करणे
    first_line = text.strip().split('\n')[0]

    name = re.split(
        r'Mobile:|Email:|Phone:',
        first_line,
        flags=re.IGNORECASE
    )[0].strip()

    name = re.sub(
        r'[^a-zA-Z .]',
        '',
        name
    ).strip()

    # Resume मधील वेगवेगळे sections शोधणे
    def get_section(section_names):

        pattern = (
            r'(?:' + '|'.join(section_names) +
            r')\s*[:\-]?\s*(.*?)(?=\n\s*[A-Z][A-Za-z /&()]{2,35}\s*[:\-]|\Z)'
        )

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE | re.DOTALL
        )

        return match.group(1).strip() if match else ""

    # Skills extract करणे
    skills = get_section([
        r'Technical Skills',
        r'Skills',
        r'Technologies'
    ])

    # Education extract करणे
    education = get_section([
        r'Education',
        r'Academic Qualification',
        r'Educational Qualification'
    ])

    # Experience extract करणे
    experience = get_section([
        r'Professional Experience',
        r'Work Experience',
        r'Experience',
        r'Internship'
    ])

    # Certifications extract करणे
    certifications = get_section([
        r'Certifications',
        r'Certificates',
        r'Certification'
    ])

    return {
        'candidate_name': name,
        'email': email,
        'phone': phone,
        'skills': skills,
        'education': education,
        'experience': experience,
        'certifications': certifications,
        'extracted_text': text
    }
