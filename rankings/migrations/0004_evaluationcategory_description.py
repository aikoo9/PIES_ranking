# Generated by Django 5.2.1 on 2025-05-10 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "rankings",
            "0003_alter_brand_options_alter_evaluationcategory_options_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="evaluationcategory",
            name="description",
            field=models.TextField(
                blank=True, null=True, verbose_name="카테고리 설명 (메모)"
            ),
        ),
    ]
