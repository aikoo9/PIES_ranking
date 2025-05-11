# rankings/views.py
from django.shortcuts import render
from .models import Brand # Brand 모델을 가져옵니다.

def brand_ranking_list(request):
    # 현재 순위(current_rank)가 있고(null이 아니고), 순위 순서대로 브랜드들을 가져옵니다.
    # current_rank가 낮은 순 (1위부터) -> 이름 순으로 정렬
    brands_ranked = Brand.objects.exclude(current_rank__isnull=True).order_by('current_rank', 'name')

    # 만약 100개로 제한하고 싶다면 (요청사항)
    # brands_ranked = brands_ranked[:100] # 상위 100개만 가져오기

    context = {
        'brands': brands_ranked,
        'page_title': '브랜드 ESG/TNFD 랭킹', # 페이지 제목 전달 (선택 사항)
    }
    return render(request, 'rankings/brand_list.html', context)