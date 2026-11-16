
import json
import PyPDF2

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ai_engine.models import ChatMessage

from ai_engine.services import (
    generate_gemini_response,
    analyze_resume,
    generate_career_roadmap
)

from ai_engine.job_search import search_company_jobs


# AI Chat API
@csrf_exempt
def ai_chat(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body)

            prompt = data.get("message", "").strip()
            candidate_info = data.get("candidate_info")
            career_roadmap = data.get("career_roadmap")
            chat_history = data.get("chat_history", [])
            session_id = data.get("session_id")

            if not prompt:
                return JsonResponse({
                    "success": False,
                    "error": "Message is required"
                }, status=400)

            if not isinstance(chat_history, list):
                chat_history = []

            response = generate_gemini_response(
                prompt=prompt,
                candidate_info=candidate_info,
                career_roadmap=career_roadmap,
                chat_history=chat_history
            )

            # Save User Message and AI Response
            if session_id:
                ChatMessage.objects.create(
                    session_id=session_id,
                    role="user",
                    message=prompt
                )

                ChatMessage.objects.create(
                    session_id=session_id,
                    role="assistant",
                    message=response
                )

            return JsonResponse({
                "success": True,
                "message": prompt,
                "response": response
            })

        except Exception as e:
            import traceback
            traceback.print_exc()

            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=500)

    return JsonResponse({
        "error": "Only POST method is allowed"
    }, status=405)


# Resume Analysis API
@csrf_exempt
def resume_analysis(request):

    if request.method == "POST":
        try:
            resume_file = request.FILES.get("resume")

            if not resume_file:
                return JsonResponse({
                    "success": False,
                    "error": "Please upload a resume PDF"
                }, status=400)

            if resume_file.size > 5 * 1024 * 1024:
                return JsonResponse({
                    "success": False,
                    "error": "File size must be below 5 MB"
                }, status=400)

            if not resume_file.name.lower().endswith(".pdf"):
                return JsonResponse({
                    "success": False,
                    "error": "Only PDF files are allowed"
                }, status=400)

            pdf_reader = PyPDF2.PdfReader(resume_file)

            resume_text = ""

            for page in pdf_reader.pages:
                resume_text += page.extract_text() or ""

            if not resume_text.strip():
                return JsonResponse({
                    "success": False,
                    "error": "Could not extract text from PDF"
                }, status=400)

            analysis_result = analyze_resume(resume_text)

            if isinstance(analysis_result, str):
                analysis_data = json.loads(analysis_result)
            else:
                analysis_data = analysis_result

            candidate_type = analysis_data.get(
                "candidate_type", "Fresher"
            )

            experience = analysis_data.get(
                "total_experience_years", 0
            )

            internship = analysis_data.get(
                "internship_experience_months", 0
            )

            skills = analysis_data.get("skills", [])
            education = analysis_data.get("education", "Not Available")
            analysis = analysis_data.get("analysis", "")
            recommended_jobs = analysis_data.get(
                "recommended_jobs", []
            )

            available_jobs = []
            job_search_error = None

            try:
                available_jobs = search_company_jobs(
                    skills,
                    experience,
                    location="India",
                    recommended_jobs=recommended_jobs
                )
            except Exception as job_error:
                job_search_error = str(job_error)

            return JsonResponse({
                "success": True,
                "candidate_type": candidate_type,
                "total_experience_years": experience,
                "internship_experience_months": internship,
                "skills": skills,
                "education": education,
                "analysis": analysis,
                "recommended_jobs": recommended_jobs,
                "available_jobs": available_jobs,
                "total_available_jobs": len(available_jobs),
                "job_search_error": job_search_error
            })

        except Exception as e:
            import traceback
            traceback.print_exc()

            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=500)

    return JsonResponse({
        "error": "Only POST method is allowed"
    }, status=405)


# AI Career Roadmap API
@csrf_exempt
def career_roadmap(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body)

            candidate_info = data.get("candidate_info", {})

            if not isinstance(candidate_info, dict):
                return JsonResponse({
                    "success": False,
                    "error": "Invalid candidate information"
                }, status=400)

            if not candidate_info.get("skills"):
                return JsonResponse({
                    "success": False,
                    "error": "Candidate skills are required"
                }, status=400)

            roadmap_result = generate_career_roadmap(
                candidate_info
            )

            if isinstance(roadmap_result, str):
                roadmap = json.loads(roadmap_result)
            else:
                roadmap = roadmap_result

            return JsonResponse({
                "success": True,
                "roadmap": roadmap
            })

        except Exception as e:
            import traceback
            traceback.print_exc()

            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=500)

    return JsonResponse({
        "error": "Only POST method is allowed"
    }, status=405)


# Chat History API
@csrf_exempt
def chat_history(request):

    if request.method == "GET":
        session_id = request.GET.get("session_id")

        if not session_id:
            return JsonResponse({
                "success": False,
                "error": "Session ID is required"
            }, status=400)

        messages = ChatMessage.objects.filter(
            session_id=session_id
        ).order_by("created_at")

        data = [
            {
                "role": msg.role,
                "text": msg.message,
                "created_at": msg.created_at.isoformat()
            }
            for msg in messages
        ]

        return JsonResponse({
            "success": True,
            "messages": data
        })

    return JsonResponse({
        "error": "Only GET method is allowed"
    }, status=405)


# Delete Chat History API
@csrf_exempt
def delete_chat_history(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            session_id = data.get("session_id")

            if not session_id:
                return JsonResponse({
                    "success": False,
                    "error": "Session ID is required"
                }, status=400)

            deleted_count, _ = ChatMessage.objects.filter(
                session_id=session_id
            ).delete()

            return JsonResponse({
                "success": True,
                "message": "Chat history deleted successfully",
                "deleted_count": deleted_count
            })

        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=500)

    return JsonResponse({
        "error": "Only POST method is allowed"
    }, status=405)
