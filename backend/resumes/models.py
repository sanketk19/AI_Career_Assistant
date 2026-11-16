from django.db import models


# Resume information database model
class Resume(models.Model):

    # Uploaded PDF file
    resume = models.FileField(upload_to='resumes/')

    # Resume upload date and time
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # Extracted text from PDF
    extracted_text = models.TextField(blank=True, null=True)

    # Candidate name
    candidate_name = models.CharField(max_length=255, blank=True, null=True)

    # Candidate email
    email = models.EmailField(blank=True, null=True)

    # Candidate phone number
    phone = models.CharField(max_length=20, blank=True, null=True)

    # Candidate skills
    skills = models.TextField(blank=True, null=True)

    # Candidate education
    education = models.TextField(blank=True, null=True)

    # Candidate work experience
    experience = models.TextField(blank=True, null=True)

    # Candidate certifications
    certifications = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.resume.name