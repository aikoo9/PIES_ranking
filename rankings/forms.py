# rankings/forms.py
from django import forms
from .models import BrandEvaluationScore, EvaluationItem


class BrandEvaluationScoreForm(forms.ModelForm):
    class Meta:
        model = BrandEvaluationScore
        fields = '__all__'
        widgets = {  # 위젯 설정을 Meta 클래스 안으로 이동
            'notes': forms.Textarea(attrs={'rows': 2, 'cols': 40}),  # 메모 필드의 세로 줄 수를 2로, 가로 크기를 40으로 지정
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'score' in self.fields:
            # 이전 __init__ 로직에서 help_text 설정 부분은 그대로 두거나,
            # "평가 항목의 점수 범위와 가중치를 확인 후 입력해주세요." 와 같이 고정된 텍스트로 설정
            self.fields['score'].help_text = "점수 범위 및 가중치는 '평가 항목 목록'에서 확인하세요."

        if 'item' in self.fields:
            self.fields['item'].queryset = EvaluationItem.objects.order_by('category__name', 'name')

    # clean_score 메소드는 이전과 동일
    def clean_score(self, *args, **kwargs):
        # ... (이전 clean_score 코드)
        score = self.cleaned_data.get('score')
        item_instance = self.cleaned_data.get('item')

        if score is not None and item_instance:
            min_val = item_instance.min_score
            max_val = item_instance.max_score
            if not (min_val <= score <= max_val):
                raise forms.ValidationError(
                    f"점수는 {min_val}점과 {max_val}점 사이여야 합니다. (입력값: {score})"
                )
        elif score is not None and not item_instance:
            raise forms.ValidationError("평가 항목을 먼저 선택해주세요.")

        return score