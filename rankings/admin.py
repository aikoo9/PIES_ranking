# rankings/admin.py
from django.contrib import admin, messages
from django.utils.html import format_html
from .models import Brand, EvaluationCategory, EvaluationItem, BrandEvaluationScore
from .forms import BrandEvaluationScoreForm  # forms.py에서 만든 폼 import

# --- 관리자 페이지 제목 및 헤더 변경 ---
admin.site.site_header = "PIES 관리자"
admin.site.site_title = "PIES 관리 포털"
admin.site.index_title = "PIES 관리 홈"
# --- 변경 끝 ---

# BrandEvaluationScore 모델을 Brand 관리자 페이지에 인라인으로 표시하기 위한 클래스
# 이 클래스는 BrandAdmin보다 먼저 정의되어야 합니다.
class BrandEvaluationScoreInline(admin.TabularInline):
    model = BrandEvaluationScore
    form = BrandEvaluationScoreForm
    extra = 1
    autocomplete_fields = ['item']
    readonly_fields = ('display_item_min_score', 'display_item_max_score', 'display_item_weight', 'evaluated_at')
    fields = ('item', 'display_item_min_score', 'display_item_max_score', 'display_item_weight', 'score', 'notes', 'evaluated_at')

    def display_item_min_score(self, obj):
        if obj.item:
            return obj.item.min_score
        return "-"
    display_item_min_score.short_description = "최소 점수"

    def display_item_max_score(self, obj):
        if obj.item:
            return obj.item.max_score
        return "-"
    display_item_max_score.short_description = "최대 점수"

    def display_item_weight(self, obj):
        if obj.item and obj.item.weight is not None:
            return f"{obj.item.weight * 100:.1f}%"
        return "-"
    display_item_weight.short_description = "가중치"


# Brand 모델 관리자 페이지 커스터마이징
class BrandAdmin(admin.ModelAdmin):
    list_display = (
        'display_logo', 'name', 'current_rank', 'previous_rank', 'total_score', 'last_activity_short',
        'last_calculated_at')
    list_display_links = ('display_logo', 'name')
    list_filter = ('current_rank',)
    search_fields = ('name',)
    inlines = [BrandEvaluationScoreInline]

    def display_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="30" height="auto" />', obj.logo.url)
        return "로고 없음"
    display_logo.short_description = "로고"

    def last_activity_short(self, obj):
        if obj.last_activity:
            return (obj.last_activity[:30] + '...') if len(obj.last_activity) > 30 else obj.last_activity
        return "-"
    last_activity_short.short_description = "마지막 활동 요약"

    def update_scores_and_ranks(self, request, queryset):
        updated_brands_count = 0
        for brand_obj in queryset:
            brand_obj.calculate_and_save_total_score()
            updated_brands_count += 1

        all_brands = Brand.objects.order_by('-total_score', 'name')

        for b in Brand.objects.all():
            b.previous_rank = b.current_rank
            b.save(update_fields=['previous_rank'])

        rank_counter = 1
        for brand_to_rank in all_brands:
            brand_to_rank.current_rank = rank_counter
            brand_to_rank.save(update_fields=['current_rank'])
            rank_counter += 1

        self.message_user(request, f"{updated_brands_count}개 브랜드의 점수가 업데이트되었고, 전체 순위가 재계산되었습니다.", messages.SUCCESS)
    update_scores_and_ranks.short_description = "선택된 브랜드 점수 및 전체 순위 업데이트"

    actions = [update_scores_and_ranks]

    fieldsets = (
        ('기본 정보', {
            'fields': ('name', 'logo', 'last_activity'),
            'classes': ('collapse',),
        }),
        ('순위 및 점수 정보', {
            'fields': ('total_score', 'current_rank', 'previous_rank', 'last_calculated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('total_score', 'current_rank', 'previous_rank', 'last_calculated_at')

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

admin.site.register(Brand, BrandAdmin)


class EvaluationCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description_short', 'get_item_count')
    search_fields = ('name', 'description')
    fields = ('name', 'description')

    def description_short(self, obj):
        if obj.description:
            return (obj.description[:50] + '...') if len(obj.description) > 50 else obj.description
        return "-"
    description_short.short_description = "카테고리 설명 (요약)"

    def get_item_count(self, obj):
        return obj.items.count()
    get_item_count.short_description = "평가 항목 수"

admin.site.register(EvaluationCategory, EvaluationCategoryAdmin)


class EvaluationItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'min_score', 'max_score', 'weight_display')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')

    def weight_display(self, obj):
        if obj.weight is not None:
            return f"{obj.weight * 100:.1f}%"
        return "-"
    weight_display.short_description = "가중치 (%)"
    weight_display.admin_order_field = 'weight'

admin.site.register(EvaluationItem, EvaluationItemAdmin)

# admin.site.register(BrandEvaluationScore) # 주석 처리 유지