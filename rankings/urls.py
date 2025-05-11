# rankings/urls.py
from django.urls import path
from . import views # 현재 앱의 views.py를 가져옵니다.

app_name = 'rankings' # URL 네임스페이스 설정

urlpatterns = [
    path('', views.brand_ranking_list, name='brand_list'),
]