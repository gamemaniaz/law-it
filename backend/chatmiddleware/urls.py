from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from chatmiddleware import views

urlpatterns = [
    path('lawyer/', views.LawyerList.as_view()),
    path('lawyer/<int:pk>/', views.LawyerDetail.as_view()),
    path('aol/', views.queryAOL),
	path('translate/', views.translate)
]

urlpatterns = format_suffix_patterns(urlpatterns)