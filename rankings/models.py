from django.db import models
from django.utils import timezone

# Create your models here.

class Brand(models.Model):
    # ... (기존 필드들은 그대로) ...
    name = models.CharField(max_length=100, unique=True, verbose_name="브랜드명")
    logo = models.ImageField(upload_to='brand_logos/', null=True, blank=True, verbose_name="로고")
    last_activity = models.TextField(null=True, blank=True, verbose_name="마지막 활동/이슈")
    current_rank = models.IntegerField(null=True, blank=True, verbose_name="현재 순위")
    previous_rank = models.IntegerField(null=True, blank=True, verbose_name="지난 순위")
    total_score = models.FloatField(null=True, blank=True, default=0.0, verbose_name="현재 종합 점수")
    last_calculated_at = models.DateTimeField(null=True, blank=True, verbose_name="마지막 순위 계산일")

    def __str__(self):
        return self.name

    def calculate_and_save_total_score(self):
        """이 브랜드의 모든 평가 점수를 기반으로 종합 점수를 계산하고 저장합니다."""
        total_weighted_score = 0
        # 이 브랜드에 연결된 모든 BrandEvaluationScore 객체들을 가져옵니다.
        # 'scores'는 BrandEvaluationScore 모델의 brand 필드에 설정한 related_name 입니다.
        evaluation_scores = self.scores.all() # scores는 BrandEvaluationScore의 related_name

        if not evaluation_scores.exists():
            self.total_score = 0.0 # 평가 점수가 없으면 0점
        else:
            for eval_score in evaluation_scores:
                if eval_score.score is not None and eval_score.item.weight is not None:
                    total_weighted_score += (eval_score.score * eval_score.item.weight)
            self.total_score = total_weighted_score

        self.last_calculated_at = timezone.now() # 현재 시간으로 업데이트
        self.save(update_fields=['total_score', 'last_calculated_at']) # 특정 필드만 업데이트
        return self.total_score

    class Meta:
        verbose_name = "브랜드"
        verbose_name_plural = "브랜드 목록"
        ordering = ['current_rank', 'name']

    # 여기에 나중에 점수 및 순위 계산 메소드를 추가할 수 있습니다.
    # 예: def calculate_total_score(self): ...
    # 예: def update_rank(self, new_rank): ...


class EvaluationCategory(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="카테고리명")
    description = models.TextField(blank=True, null=True, verbose_name="카테고리 설명 (메모)")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "평가 카테고리"
        verbose_name_plural = "평가 카테고리 목록"
        ordering = ['name'] # 카테고리명으로 정렬


class EvaluationItem(models.Model):
    category = models.ForeignKey(EvaluationCategory, on_delete=models.CASCADE, related_name='items', verbose_name="카테고리")
    name = models.CharField(max_length=100, verbose_name="평가 항목명")
    description = models.TextField(blank=True, null=True, verbose_name="설명")
    min_score = models.IntegerField(default=0, verbose_name="최소 점수")
    max_score = models.IntegerField(default=10, verbose_name="최대 점수")
    weight = models.FloatField(default=0.0, verbose_name="가중치", help_text="예: 0.2는 20%를 의미합니다.") # help_text 추가

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    class Meta:
        verbose_name = "평가 항목"
        verbose_name_plural = "평가 항목 목록"
        ordering = ['category__name', 'name'] # 카테고리명, 그 다음 평가 항목명으로 정렬 (category.name 대신 category__name 사용)


class BrandEvaluationScore(models.Model):
    # ... (필드 정의는 그대로) ...
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='scores', verbose_name="브랜드")
    item = models.ForeignKey(EvaluationItem, on_delete=models.CASCADE, related_name='scores', verbose_name="평가 항목")
    score = models.IntegerField(verbose_name="점수", null=True, blank=True)
    evaluated_at = models.DateTimeField(auto_now_add=True, verbose_name="평가일")
    notes = models.TextField(blank=True, null=True, verbose_name="메모")  # 메모 필드 추가

    def __str__(self):
        brand_name = "N/A"
        item_name = "N/A"
        score_display = str(self.score) if self.score is not None else "미입력"

        # self.brand 가 존재하고, self.brand.pk 가 존재할 때 (즉, DB에 저장된 Brand 객체일 때)
        if hasattr(self, 'brand') and self.brand and hasattr(self.brand, 'pk') and self.brand.pk:
            brand_name = self.brand.name

        # self.item 이 존재하고, self.item.pk 가 존재할 때
        if hasattr(self, 'item') and self.item and hasattr(self.item, 'pk') and self.item.pk:
            item_name = self.item.name
            # 만약 item의 카테고리까지 표시하고 싶다면:
            # item_name = f"{self.item.category.name} - {self.item.name}"

        return f"{brand_name} - {item_name}: {score_display}"