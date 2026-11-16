
# Django REST Framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

# Resume model आणि serializer
from .models import Resume
from .serializers import ResumeUploadSerializer

# PDF extraction functions
from .utils import extract_text_from_pdf, extract_resume_details


# Resume Upload API
class ResumeUploadView(APIView):

    # PDF upload स्वीकारणे
    parser_classes = [MultiPartParser, FormParser]

    # POST request
    def post(self, request):

        # Resume validation
        serializer = ResumeUploadSerializer(data=request.data)

        if serializer.is_valid():

            # Uploaded PDF मिळवणे
            resume_file = serializer.validated_data['resume']

            # PDF मधून text extract करणे
            extracted_text = extract_text_from_pdf(resume_file)

            # सर्व Resume details extract करणे
            details = extract_resume_details(extracted_text)

            # सर्व माहिती database मध्ये save करणे
            saved_resume = Resume.objects.create(
                resume=resume_file,
                extracted_text=details['extracted_text'],
                candidate_name=details['candidate_name'],
                email=details['email'],
                phone=details['phone'],
                skills=details['skills'],
                education=details['education'],
                experience=details['experience'],
                certifications=details['certifications']
            )

            # Success response
            return Response({
                'message': 'Resume uploaded and analyzed successfully!',
                'id': saved_resume.id,
                'filename': saved_resume.resume.name,
                'candidate_name': saved_resume.candidate_name,
                'email': saved_resume.email,
                'phone': saved_resume.phone,
                'skills': saved_resume.skills,
                'education': saved_resume.education,
                'experience': saved_resume.experience,
                'certifications': saved_resume.certifications
            }, status=status.HTTP_200_OK)

        # Validation error
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
