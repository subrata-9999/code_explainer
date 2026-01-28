from django.urls import path
from .views import test_ai, index, explain_code


urlpatterns = [
    path("", index),
    path("test-ai/", test_ai),
    path("explain/", explain_code, name="explain_code"),
]
