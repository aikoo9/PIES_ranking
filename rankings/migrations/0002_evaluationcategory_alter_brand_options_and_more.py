# Generated by Django 5.2.1 on 2025-05-10 17:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rankings", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="EvaluationCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
            ],
            options={
                "verbose_name": "평가 카테고리",
                "verbose_name_plural": "평가 카테고리 목록",
            },
        ),
        migrations.AlterModelOptions(
            name="brand",
            options={"verbose_name": "브랜드", "verbose_name_plural": "브랜드 목록"},
        ),
        migrations.AlterField(
            model_name="brand",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.CreateModel(
            name="EvaluationItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="설명"),
                ),
                ("min_score", models.IntegerField(default=0, verbose_name="최소 점수")),
                (
                    "max_score",
                    models.IntegerField(default=10, verbose_name="최대 점수"),
                ),
                ("weight", models.FloatField(default=0.0, verbose_name="가중치")),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="rankings.evaluationcategory",
                        verbose_name="카테고리",
                    ),
                ),
            ],
            options={
                "verbose_name": "평가 항목",
                "verbose_name_plural": "평가 항목 목록",
                "ordering": ["category", "name"],
            },
        ),
    ]
