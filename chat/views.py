from django.http import JsonResponse
from .services.gemini_client import explain_with_gemini, test_gemini_connection
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import os
from django.views.decorators.csrf import csrf_exempt
import json

# def index(request):
#     return render(request, "chat/index.html")

def index(request):
    template_path = os.path.join(settings.BASE_DIR, "templates", "chat", "index.html")
    return HttpResponse(open(template_path).read())

def test_ai(request):
    result = test_gemini_connection()
    return JsonResponse({"ai_response": result})


@csrf_exempt
def explain_code(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "Invalid request method"},
            status=405
        )

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON body"},
            status=400
        )

    code = body.get("code", "").strip()
    language = body.get("language", "code")

    if not code:
        return JsonResponse(
            {"error": "Code is required"},
            status=400
        )

    prompt = f"""
        Explain the following {language} code clearly and simply:

        {code}
        """

    explanation = explain_with_gemini(prompt)
    print("Gemini result:", explanation)

    if not explanation:
        # ✅ AI failure but backend OK
        return JsonResponse({
            "error": "AI could not generate a response right now. Please try again."
        }, status=200)

    return JsonResponse({
        "explanation": explanation
    })
